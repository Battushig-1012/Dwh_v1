"""BCBS 239 (Jan 2013) additive APIs — complements /api/rdarr (SSM)."""

from fastapi import APIRouter, Depends, HTTPException

from .. import bcbs239_demo as bc
from ..auth.deps import get_current_user
from ..config import settings

router = APIRouter()


def _demo():
    if not settings.demo_mode:
        raise HTTPException(501, "BCBS pack available in DEMO_MODE")


@router.get("/principles")
def principles(_user: dict = Depends(get_current_user)):
    """P1–P14 compliance overview."""
    _demo()
    return bc.principles_overview()


@router.get("/governance-extras")
def governance_extras(_user: dict = Depends(get_current_user)):
    """P1 extras: limitations, trade-offs, expert judgment, materiality, change checklist."""
    _demo()
    return {
        "limitations": bc.LIMITATIONS,
        "tradeoffs": bc.TRADEOFFS,
        "expert_judgments": bc.EXPERT_JUDGMENTS,
        "materiality_policy": bc.MATERIALITY_POLICY,
        "change_checklist": bc.CHANGE_CHECKLIST,
    }


@router.get("/architecture")
def architecture(_user: dict = Depends(get_current_user)):
    """P2: single IDs, authoritative sources, BCP."""
    _demo()
    return {
        "single_identifiers": bc.SINGLE_IDENTIFIERS,
        "authoritative_sources": bc.AUTHORITATIVE_SOURCES,
        "bcp": bc.BCP_RDARR,
    }


@router.get("/validation-inventory")
def validation_inventory(_user: dict = Depends(get_current_user)):
    """P3/P7: validation rules inventory, accuracy requirements, escalation."""
    _demo()
    return {
        "rules": bc.VALIDATION_RULES_INVENTORY,
        "accuracy_requirements": bc.ACCURACY_REQUIREMENTS,
        "escalation": bc.DQ_ESCALATION,
    }


@router.get("/completeness")
def completeness(_user: dict = Depends(get_current_user)):
    """P4: completeness matrix + concentrations."""
    _demo()
    return {
        "matrix": bc.COMPLETENESS_MATRIX,
        "concentrations": bc.CONCENTRATIONS,
    }


@router.get("/risk-report")
def risk_report(_user: dict = Depends(get_current_user)):
    """P8/P9 comprehensive risk report with forward-looking scenarios."""
    _demo()
    return bc.comprehensive_risk_report()


@router.get("/recipients")
def recipients(_user: dict = Depends(get_current_user)):
    """P9 recipient-tailored needs + confirmation."""
    _demo()
    return bc.RECIPIENT_PROFILES


@router.get("/frequency-matrix")
def frequency_matrix(_user: dict = Depends(get_current_user)):
    """P10 normal vs stress frequency escalation."""
    _demo()
    return bc.FREQUENCY_MATRIX


@router.get("/distribution")
def distribution(_user: dict = Depends(get_current_user)):
    """P11 distribution list, classification, delivery/ack."""
    _demo()
    return bc.DISTRIBUTION
