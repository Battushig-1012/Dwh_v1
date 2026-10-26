"""
Nightly ETL orchestrator (Airflow-equivalent CLI).
Schedule: 02:00 — produce fresh marts by 09:00 (BCBS 239 Timeliness).
"""

from __future__ import annotations

import logging
import sys
import uuid
from datetime import date

from .config import settings
from .extractors.demo_sources import extract_demo_borrowers, extract_demo_journal, extract_demo_loans
from .loaders.postgres_loader import PostgresLoader
from .quality.engine import DataQualityEngine
from .transformers.core_transforms import build_credit_mart, to_core_loans

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("etl.nightly")


def run(as_of: date | None = None) -> int:
    as_of = as_of or date.today()
    batch_id = uuid.uuid4()
    loader = PostgresLoader(settings.database_url)
    sources = ["CORE_DB", "ERP_ACC", "LOAN_APP"]

    log.info("Starting batch %s as_of=%s demo=%s", batch_id, as_of, settings.use_demo_sources)
    loader.start_batch(batch_id, sources)

    try:
        if settings.use_demo_sources or not settings.core_db_url:
            loans = extract_demo_loans(as_of)
            journal = extract_demo_journal(as_of)
            borrowers = extract_demo_borrowers()
        else:
            raise NotImplementedError("Wire CORE_DB_URL / ERP_DB_URL extractors for production")

        extracted = len(loans) + len(journal) + len(borrowers)

        # Staging landing (raw mirror — no business transforms)
        now = pd_now()
        loader.load_staging("stg_core_loans", loans.assign(**{"_extracted_at": now}), batch_id, "CORE_DB")
        loader.load_staging("stg_acc_journal", journal.assign(**{"_extracted_at": now}), batch_id, "ERP_ACC")
        loader.load_staging("stg_app_borrowers", borrowers.assign(**{"_extracted_at": now}), batch_id, "LOAN_APP")

        # Data quality on loans
        dq = DataQualityEngine("stg_core_loans")
        clean = dq.null_check(loans, ["loan_id", "customer_id", "principal_amount", "outstanding_balance"])
        clean = dq.range_check(clean, "interest_rate", min_value=0)
        clean = dq.range_check(clean, "principal_amount", min_value=0.01)
        clean = dq.range_check(clean, "outstanding_balance", min_value=0)
        clean = dq.uniqueness_check(clean, ["loan_id"])
        loader.save_dq_results(batch_id, dq.results)

        if dq.has_critical_failures():
            loader.finish_batch(batch_id, "FAILED", extracted, 0, extracted - len(clean), "Critical DQ failures")
            log.error("Critical DQ failures — aborting load")
            return 1

        core = to_core_loans(clean, batch_id, as_of)
        loaded = loader.upsert_core_loans(core)

        # Refresh credit mart from all loans for as_of (seed + new)
        all_loans = loader.latest_as_of_loans(as_of)
        if all_loans.empty:
            all_loans = core
        mart = build_credit_mart(all_loans, batch_id, as_of)
        loader.upsert_credit_mart(mart)

        rejected = extracted - len(clean)
        loader.finish_batch(batch_id, "SUCCESS", extracted, loaded, max(rejected, 0))
        loader.write_audit(
            "etl_nightly",
            "BATCH_COMPLETE",
            "etl_batch",
            str(batch_id),
            {"as_of": str(as_of), "loaded": loaded, "npl_ratio": mart["npl_ratio_pct"]},
        )
        log.info("Batch SUCCESS loaded=%s npl_ratio=%.4f", loaded, mart["npl_ratio_pct"])
        return 0
    except Exception as exc:  # noqa: BLE001
        log.exception("Batch failed")
        loader.finish_batch(batch_id, "FAILED", 0, 0, 0, str(exc))
        return 1


def pd_now():
    from datetime import datetime

    return datetime.utcnow()


if __name__ == "__main__":
    sys.exit(run())
