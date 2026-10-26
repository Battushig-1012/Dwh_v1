"""EBA/GL/2021/05 — Internal governance under CRD APIs."""

from fastapi import APIRouter, Depends, HTTPException

from .. import internal_gov_demo as ig
from ..auth.deps import get_current_user
from ..config import settings

router = APIRouter()


def _demo():
    if not settings.demo_mode:
        raise HTTPException(501, "Internal governance pack currently available in DEMO_MODE")


@router.get("/overview")
def overview(_user: dict = Depends(get_current_user)):
    _demo()
    return ig.overview()


@router.get("/management-body")
def management_body(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "management_body": ig.MANAGEMENT_BODY,
        "committees": ig.COMMITTEES,
        "meeting_pack": ig.MEETING_PACK,
    }


@router.get("/organisation")
def organisation(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "structure": ig.ORG_STRUCTURE,
        "proportionality": ig.PROPORTIONALITY,
    }


@router.get("/conduct")
def conduct(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "risk_culture": ig.RISK_CULTURE,
        "conflicts_of_interest": ig.CONFLICTS_OF_INTEREST,
        "whistleblowing": ig.WHISTLEBLOWING,
    }


@router.get("/controls")
def controls(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "three_lines": ig.THREE_LINES,
        "control_functions": ig.CONTROL_FUNCTIONS,
        "new_products": ig.NEW_PRODUCTS,
        "internal_control_framework": ig.INTERNAL_CONTROL_FRAMEWORK,
    }


@router.get("/bcm-transparency")
def bcm_transparency(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "bcm": ig.BCM_GOVERNANCE,
        "transparency": ig.TRANSPARENCY,
    }
