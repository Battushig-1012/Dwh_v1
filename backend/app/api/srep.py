from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import demo_data
from ..auth.deps import get_current_user
from ..config import settings
from ..db import get_db

router = APIRouter()


@router.get("/overview")
def srep_overview(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.srep_overview()

    assert db is not None
    capital = db.execute(
        text(
            """
            SELECT as_of_date, tier1_capital, tier2_capital, total_capital,
                   risk_weighted_assets, car_pct, regulatory_minimum, buffer_pct
            FROM data_marts.mart_srep_capital_adequacy
            ORDER BY as_of_date DESC LIMIT 1
            """
        )
    ).mappings().first()

    credit = db.execute(
        text(
            """
            SELECT as_of_date, total_loans, total_outstanding, performing_balance,
                   watch_balance, npl_balance, npl_ratio_pct, avg_dpd, avg_interest_rate
            FROM data_marts.mart_srep_credit_portfolio
            ORDER BY as_of_date DESC LIMIT 1
            """
        )
    ).mappings().first()

    liquidity = db.execute(
        text(
            """
            SELECT as_of_date, liquid_assets, short_term_liab, lcr_pct, regulatory_minimum
            FROM data_marts.mart_srep_liquidity
            ORDER BY as_of_date DESC LIMIT 1
            """
        )
    ).mappings().first()

    return {
        "capital": dict(capital) if capital else None,
        "credit": dict(credit) if credit else None,
        "liquidity": dict(liquidity) if liquidity else None,
        "pillars": [
            {"code": "CAPITAL", "name_mn": "Капитал", "value": float(capital["car_pct"]) if capital else None, "unit": "%", "threshold": 12.0},
            {"code": "LIQUIDITY", "name_mn": "Хөрвөх чадвар", "value": float(liquidity["lcr_pct"]) if liquidity else None, "unit": "%", "threshold": 100.0},
            {"code": "CREDIT", "name_mn": "Зээлийн чанар", "value": float(credit["avg_dpd"]) if credit else None, "unit": "DPD", "threshold": 30.0},
            {"code": "NPL", "name_mn": "NPL харьцаа", "value": float(credit["npl_ratio_pct"]) if credit else None, "unit": "%", "threshold": 5.0},
        ],
    }


@router.get("/loans")
def loan_snapshot(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.LOANS
    assert db is not None
    rows = db.execute(
        text(
            """
            SELECT loan_id, customer_id, product_code, outstanding_balance,
                   interest_rate, days_past_due, status_code, npl_flag, as_of_date,
                   sys_source_system, sys_batch_id
            FROM dw_core.fact_loan
            WHERE as_of_date = (SELECT MAX(as_of_date) FROM dw_core.fact_loan)
            ORDER BY outstanding_balance DESC
            """
        )
    ).mappings().all()
    return [dict(r) for r in rows]


@router.get("/m1")
def mongolbank_m1(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.M1
    assert db is not None
    rows = db.execute(
        text(
            """
            SELECT reporting_period, dpm_code, dpm_label_mn, dpm_label_en,
                   amount_mnt, formula_ref, source_mart
            FROM data_marts.mart_reg_mongolbank_m1
            WHERE reporting_period = (
                SELECT MAX(reporting_period) FROM data_marts.mart_reg_mongolbank_m1
            )
            ORDER BY dpm_code
            """
        )
    ).mappings().all()
    return [dict(r) for r in rows]
