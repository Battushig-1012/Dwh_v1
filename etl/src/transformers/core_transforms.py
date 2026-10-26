from __future__ import annotations

import hashlib
from datetime import date
from uuid import UUID

import pandas as pd


def hash_row(parts: list[str]) -> str:
    payload = "|".join("" if p is None else str(p) for p in parts)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def to_core_loans(df: pd.DataFrame, batch_id: UUID, as_of: date, source: str = "CORE_DB") -> pd.DataFrame:
    out = df.copy()
    out["as_of_date"] = as_of
    out["sys_source_system"] = source
    out["sys_batch_id"] = str(batch_id)
    out["sys_hash_key"] = out.apply(
        lambda r: hash_row(
            [r["loan_id"], r["outstanding_balance"], r["days_past_due"], r["status_code"], str(as_of)]
        ),
        axis=1,
    )
    return out


def to_core_customers(df: pd.DataFrame, batch_id: UUID, source: str = "LOAN_APP") -> pd.DataFrame:
    out = df.rename(columns={"borrower_id": "customer_id"}).copy()
    out["sys_source_system"] = source
    out["sys_batch_id"] = str(batch_id)
    out["sys_hash_key"] = out.apply(
        lambda r: hash_row([r["customer_id"], r.get("register_no"), r["full_name"], r.get("credit_score")]),
        axis=1,
    )
    return out


def build_credit_mart(loans: pd.DataFrame, batch_id: UUID, as_of: date) -> dict:
    total_outstanding = float(loans["outstanding_balance"].sum())
    npl = loans[loans["days_past_due"] >= 90]
    watch = loans[(loans["days_past_due"] >= 30) & (loans["days_past_due"] < 90)]
    performing = loans[loans["days_past_due"] < 30]
    npl_bal = float(npl["outstanding_balance"].sum())
    return {
        "as_of_date": as_of,
        "total_loans": int(len(loans)),
        "total_outstanding": total_outstanding,
        "performing_balance": float(performing["outstanding_balance"].sum()),
        "watch_balance": float(watch["outstanding_balance"].sum()),
        "npl_balance": npl_bal,
        "npl_ratio_pct": round((npl_bal / total_outstanding) * 100, 4) if total_outstanding else 0.0,
        "avg_dpd": round(float(loans["days_past_due"].mean()), 2) if len(loans) else 0.0,
        "avg_interest_rate": round(float(loans["interest_rate"].mean()), 4) if len(loans) else 0.0,
        "sys_batch_id": str(batch_id),
    }
