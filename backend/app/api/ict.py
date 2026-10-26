"""EBA/GL/2019/04 ICT & security risk management APIs."""

from fastapi import APIRouter, Depends, HTTPException

from .. import ict_security_demo as ict
from ..auth.deps import get_current_user, require_roles
from ..config import settings

router = APIRouter()


def _demo():
    if not settings.demo_mode:
        raise HTTPException(501, "ICT security pack available in DEMO_MODE")


@router.get("/overview")
def overview(_user: dict = Depends(get_current_user)):
    _demo()
    return ict.overview()


@router.get("/strategy")
def strategy(_user: dict = Depends(get_current_user)):
    _demo()
    return {"strategy": ict.ICT_STRATEGY, "governance": ict.GOVERNANCE}


@router.get("/assets")
def assets(_user: dict = Depends(get_current_user)):
    _demo()
    return {"assets": ict.ICT_ASSETS, "risks": ict.RISK_REGISTER}


@router.get("/information-security")
def information_security(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "policy": ict.INFORMATION_SECURITY_POLICY,
        "logical_access": ict.LOGICAL_ACCESS,
        "physical": ict.PHYSICAL_SECURITY,
        "operations_security": ict.OPERATIONS_SECURITY,
        "monitoring": ict.SECURITY_MONITORING,
        "testing": ict.SECURITY_TESTING,
        "awareness": ict.AWARENESS,
    }


@router.get("/operations")
def operations(_user: dict = Depends(get_current_user)):
    _demo()
    return {
        "operations": ict.OPERATIONS,
        "incidents": ict.INCIDENTS,
        "incident_process": ict.INCIDENT_PROCESS,
        "third_parties": ict.THIRD_PARTIES,
    }


@router.get("/change")
def change_and_projects(_user: dict = Depends(get_current_user)):
    _demo()
    return {"changes": ict.ICT_CHANGES, "projects": ict.ICT_PROJECTS}


@router.get("/bcm")
def bcm(_user: dict = Depends(get_current_user)):
    _demo()
    return {"bia": ict.BIA, "bcm": ict.BCM}


@router.get("/audit")
def audit(_user: dict = Depends(get_current_user)):
    _demo()
    return ict.AUDIT


@router.get("/privileged-log")
def privileged_log(user: dict = Depends(require_roles("ADMIN", "AUDITOR", "RISK"))):
    """3.4.2(d) — privileged / security-relevant activity log."""
    _demo()
    return ict.PRIVILEGED_ACCESS_LOG
