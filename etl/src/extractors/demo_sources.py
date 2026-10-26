"""Demo source extracts when CORE_DB / ERP / Loan App are not yet connected."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pandas as pd


def extract_demo_loans(as_of: date | None = None) -> pd.DataFrame:
    as_of = as_of or date.today()
    rows = [
        ("L2001", "C010", "CONS", 8_000_000, 6_500_000, 24.0, as_of - timedelta(days=200), as_of + timedelta(days=400), 0, "ACTIVE", "UB01"),
        ("L2002", "C011", "SME", 30_000_000, 28_000_000, 21.5, as_of - timedelta(days=400), as_of + timedelta(days=200), 30, "WATCH", "UB02"),
        ("L2003", "C012", "AUTO", 12_000_000, 5_000_000, 19.0, as_of - timedelta(days=500), as_of + timedelta(days=100), 0, "ACTIVE", "DN01"),
        ("L2004", "C013", "CONS", 4_000_000, 3_800_000, 27.0, as_of - timedelta(days=150), as_of + timedelta(days=200), 110, "NPL", "UB01"),
    ]
    df = pd.DataFrame(
        rows,
        columns=[
            "loan_id", "customer_id", "product_code", "principal_amount",
            "outstanding_balance", "interest_rate", "disbursement_date",
            "maturity_date", "days_past_due", "status_code", "branch_code",
        ],
    )
    df["currency_code"] = "MNT"
    df["source_updated_at"] = datetime.utcnow()
    return df


def extract_demo_journal(as_of: date | None = None) -> pd.DataFrame:
    as_of = as_of or date.today()
    period = as_of.strftime("%Y-%m")
    rows = [
        ("J1001", "3010", "Tier1 Capital", 0, 5_100_000_000, as_of, period, "Equity closing"),
        ("J1002", "3020", "Tier2 Capital", 0, 750_000_000, as_of, period, "Subordinated debt"),
        ("J1003", "1100", "Cash & Liquid", 1_150_000_000, 0, as_of, period, "Liquid assets"),
    ]
    df = pd.DataFrame(
        rows,
        columns=[
            "journal_id", "account_code", "account_name", "debit_amount",
            "credit_amount", "posting_date", "fiscal_period", "description",
        ],
    )
    df["source_updated_at"] = datetime.utcnow()
    return df


def extract_demo_borrowers() -> pd.DataFrame:
    rows = [
        ("C010", "УБ91010111", "Нарантуяа Б.", "99001122", 2_200_000, "EMPLOYED", 710, "A010", "APPROVED"),
        ("C011", "УБ87070707", "Ганбат С.", "88001122", 3_500_000, "SELF_EMP", 690, "A011", "APPROVED"),
        ("C012", "ХӨ93030303", "Мөнхзул Т.", "77001122", 2_800_000, "EMPLOYED", 750, "A012", "APPROVED"),
        ("C013", "ДД86060606", "Энхбаяр Д.", "95001122", 1_200_000, "EMPLOYED", 540, "A013", "APPROVED"),
    ]
    df = pd.DataFrame(
        rows,
        columns=[
            "borrower_id", "register_no", "full_name", "phone", "income_monthly",
            "employment_status", "credit_score", "application_id", "application_status",
        ],
    )
    df["source_updated_at"] = datetime.utcnow()
    return df
