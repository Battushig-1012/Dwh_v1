"""SSM RDARR Guide APIs — Sections 3.1–3.7."""

from fastapi import APIRouter, Depends, HTTPException, Query

from ..auth.deps import get_current_user
from ..config import settings
from .. import rdarr_demo as rd

router = APIRouter()


def _require_demo():
    if not settings.demo_mode:
        # Live PG path can be wired later; for now RDARR pack is demo-first
        raise HTTPException(
            status_code=501,
            detail="RDARR pack currently available in DEMO_MODE. Set DEMO_MODE=true or migrate tables.",
        )


@router.get("/management-pack")
def management_pack(_user: dict = Depends(get_current_user)):
    """3.1 — Management body pack: KRIs, DQ KPIs, issues, timeliness, programme."""
    _require_demo()
    return rd.management_pack()


@router.get("/scope")
def scope_of_application(_user: dict = Depends(get_current_user)):
    """3.2 — Reports, models, KRIs, critical data elements."""
    _require_demo()
    return rd.SCOPE


@router.get("/governance")
def governance_framework(_user: dict = Depends(get_current_user)):
    """3.3 — Roles across 1LOD / central DG / 2LOD / 3LOD."""
    _require_demo()
    return {
        "management_body": rd.MANAGEMENT_BODY,
        "roles": rd.GOVERNANCE_ROLES,
    }


@router.get("/attribute-lineage")
def attribute_lineage(
    cde_id: str | None = Query(None),
    _user: dict = Depends(get_current_user),
):
    """3.4 — Attribute-level lineage for critical data elements."""
    _require_demo()
    rows = rd.ATTRIBUTE_LINEAGE
    if cde_id:
        rows = [r for r in rows if r["cde_id"] == cde_id]
    return {"lineages": rows, "cdes": rd.SCOPE["critical_data_elements"]}


@router.get("/dq-kpis")
def dq_kpis(_user: dict = Depends(get_current_user)):
    """3.5 — DQ indicators: accuracy, integrity, completeness, timeliness."""
    _require_demo()
    return {"kpis": rd.DQ_KPIS, "reconciliations": rd.RECONCILIATIONS}


@router.get("/dq-issues")
def dq_issues(_user: dict = Depends(get_current_user)):
    """3.5 — Data quality issue register."""
    _require_demo()
    return rd.DQ_ISSUES


@router.get("/workarounds")
def manual_workarounds(_user: dict = Depends(get_current_user)):
    """3.5 — EUC / manual workaround register with controls."""
    _require_demo()
    return rd.MANUAL_WORKAROUNDS


@router.get("/timeliness")
def timeliness(_user: dict = Depends(get_current_user)):
    """3.6 — Reporting calendar, production SLA, stress capability."""
    _require_demo()
    return {
        "calendar": rd.REPORTING_CALENDAR,
        "stress": rd.STRESS_CAPABILITY,
        "ecb_note": "Monthly/quarterly internal risk reports should generally not exceed 20 working days production time.",
    }


@router.get("/programme")
def implementation_programme(_user: dict = Depends(get_current_user)):
    """3.7 — RDARR implementation programme & BCBS 239 self-assessment."""
    _require_demo()
    return {
        "programme": rd.IMPLEMENTATION_PROGRAMME,
        "bcbs239": rd.BCBS239_SELF_ASSESSMENT,
    }


@router.get("/kris")
def key_risk_indicators(_user: dict = Depends(get_current_user)):
    """Risk appetite KRIs with breach status."""
    _require_demo()
    return [{**k, "status": rd.kri_status(k)} for k in rd.SCOPE["kris"]]


@router.post("/fire-drill/{scenario_code}")
def run_fire_drill(scenario_code: str, _user: dict = Depends(get_current_user)):
    """3.6 adaptability — simulate ad-hoc stress aggregation."""
    _require_demo()
    scenario = next((s for s in rd.STRESS_CAPABILITY["scenarios"] if s["code"] == scenario_code), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Unknown fire-drill scenario")
    return {
        "scenario": scenario,
        "status": "COMPLETED",
        "ran_at": rd.AS_OF,
        "result": {
            "rows_aggregated": 6 if scenario_code == "FD_CREDIT_CONC" else 3,
            "sla_hours": scenario["sla_hours"],
            "within_sla": True,
            "message": "Demo fire-drill aggregation completed from dw_core / marts snapshot",
        },
    }
