from __future__ import annotations

import json
from datetime import date
from uuid import UUID

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from ..quality.engine import DQResult


class PostgresLoader:
    def __init__(self, database_url: str):
        self.engine: Engine = create_engine(database_url)

    def start_batch(self, batch_id: UUID, sources: list[str]) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO staging.etl_batch_log (batch_id, dag_run_id, status, source_systems)
                    VALUES (:bid, :run, 'RUNNING', :sources)
                    ON CONFLICT (batch_id) DO NOTHING
                    """
                ),
                {"bid": str(batch_id), "run": f"cli_{batch_id}", "sources": sources},
            )

    def finish_batch(
        self,
        batch_id: UUID,
        status: str,
        rows_extracted: int,
        rows_loaded: int,
        rows_rejected: int,
        error: str | None = None,
    ) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    UPDATE staging.etl_batch_log
                    SET finished_at = NOW(),
                        status = :status,
                        rows_extracted = :ex,
                        rows_loaded_core = :ld,
                        rows_rejected = :rj,
                        error_message = :err
                    WHERE batch_id = :bid
                    """
                ),
                {
                    "status": status,
                    "ex": rows_extracted,
                    "ld": rows_loaded,
                    "rj": rows_rejected,
                    "err": error,
                    "bid": str(batch_id),
                },
            )

    def load_staging(self, table: str, df: pd.DataFrame, batch_id: UUID, source: str) -> int:
        if df.empty:
            return 0
        payload = df.copy()
        payload["_batch_id"] = str(batch_id)
        payload["_source_system"] = source
        payload.to_sql(table, self.engine, schema="staging", if_exists="append", index=False, method="multi")
        return len(payload)

    def upsert_core_loans(self, df: pd.DataFrame) -> int:
        if df.empty:
            return 0
        cols = [
            "loan_id", "customer_id", "product_code", "principal_amount", "outstanding_balance",
            "interest_rate", "disbursement_date", "maturity_date", "days_past_due", "status_code",
            "currency_code", "branch_code", "as_of_date", "sys_source_system", "sys_batch_id", "sys_hash_key",
        ]
        sql = text(
            """
            INSERT INTO dw_core.fact_loan (
                loan_id, customer_id, product_code, principal_amount, outstanding_balance,
                interest_rate, disbursement_date, maturity_date, days_past_due, status_code,
                currency_code, branch_code, as_of_date, sys_source_system, sys_batch_id, sys_hash_key
            ) VALUES (
                :loan_id, :customer_id, :product_code, :principal_amount, :outstanding_balance,
                :interest_rate, :disbursement_date, :maturity_date, :days_past_due, :status_code,
                :currency_code, :branch_code, :as_of_date, :sys_source_system, :sys_batch_id, :sys_hash_key
            )
            ON CONFLICT (loan_id, as_of_date) DO UPDATE SET
                outstanding_balance = EXCLUDED.outstanding_balance,
                days_past_due = EXCLUDED.days_past_due,
                status_code = EXCLUDED.status_code,
                sys_updated_at = NOW(),
                sys_batch_id = EXCLUDED.sys_batch_id,
                sys_hash_key = EXCLUDED.sys_hash_key
            """
        )
        records = df[cols].to_dict(orient="records")
        with self.engine.begin() as conn:
            conn.execute(sql, records)
        return len(records)

    def upsert_credit_mart(self, mart: dict) -> None:
        sql = text(
            """
            INSERT INTO data_marts.mart_srep_credit_portfolio (
                as_of_date, total_loans, total_outstanding, performing_balance, watch_balance,
                npl_balance, npl_ratio_pct, avg_dpd, avg_interest_rate, sys_batch_id
            ) VALUES (
                :as_of_date, :total_loans, :total_outstanding, :performing_balance, :watch_balance,
                :npl_balance, :npl_ratio_pct, :avg_dpd, :avg_interest_rate, :sys_batch_id
            )
            ON CONFLICT (as_of_date) DO UPDATE SET
                total_loans = EXCLUDED.total_loans,
                total_outstanding = EXCLUDED.total_outstanding,
                performing_balance = EXCLUDED.performing_balance,
                watch_balance = EXCLUDED.watch_balance,
                npl_balance = EXCLUDED.npl_balance,
                npl_ratio_pct = EXCLUDED.npl_ratio_pct,
                avg_dpd = EXCLUDED.avg_dpd,
                avg_interest_rate = EXCLUDED.avg_interest_rate,
                sys_batch_id = EXCLUDED.sys_batch_id,
                sys_created_at = NOW()
            """
        )
        with self.engine.begin() as conn:
            conn.execute(sql, mart)

    def save_dq_results(self, batch_id: UUID, results: list[DQResult]) -> None:
        if not results:
            return
        sql = text(
            """
            INSERT INTO governance.dq_rule_results
                (batch_id, rule_code, rule_name, target_table, severity, passed, failed_rows, total_rows, details)
            VALUES
                (:batch_id, :rule_code, :rule_name, :target_table, :severity, :passed, :failed_rows, :total_rows, CAST(:details AS jsonb))
            """
        )
        rows = [
            {
                "batch_id": str(batch_id),
                "rule_code": r.rule_code,
                "rule_name": r.rule_name,
                "target_table": r.target_table,
                "severity": r.severity,
                "passed": r.passed,
                "failed_rows": r.failed_rows,
                "total_rows": r.total_rows,
                "details": json.dumps(r.details),
            }
            for r in results
        ]
        with self.engine.begin() as conn:
            conn.execute(sql, rows)

    def write_audit(self, actor: str, action: str, entity_type: str, entity_id: str, after: dict) -> None:
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """
                    INSERT INTO governance.audit_trail (actor, action, entity_type, entity_id, after_state)
                    VALUES (:actor, :action, :etype, :eid, CAST(:after AS jsonb))
                    """
                ),
                {
                    "actor": actor,
                    "action": action,
                    "etype": entity_type,
                    "eid": entity_id,
                    "after": json.dumps(after),
                },
            )

    def latest_as_of_loans(self, as_of: date) -> pd.DataFrame:
        return pd.read_sql(
            text("SELECT * FROM dw_core.fact_loan WHERE as_of_date = :d"),
            self.engine,
            params={"d": as_of},
        )
