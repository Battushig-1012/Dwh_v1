"""EBA DPM (Aug 2013) metadata & fact APIs."""

from fastapi import APIRouter, Depends, HTTPException

from .. import dpm_demo as dpm
from ..auth.deps import get_current_user
from ..config import settings

router = APIRouter()


def _demo():
    if not settings.demo_mode:
        raise HTTPException(501, "DPM pack currently available in DEMO_MODE")


@router.get("/overview")
def overview(_user: dict = Depends(get_current_user)):
    _demo()
    return dpm.overview()


@router.get("/table/m1")
def table_m1(_user: dict = Depends(get_current_user)):
    """Template layout: Axis X/Y, cells, datapoints, facts."""
    _demo()
    return dpm.table_render()


@router.get("/dictionary")
def dictionary(_user: dict = Depends(get_current_user)):
    _demo()
    return dpm.browse_dictionary()


@router.get("/datapoints/{data_point_id}")
def datapoint(data_point_id: int, _user: dict = Depends(get_current_user)):
    _demo()
    detail = dpm.datapoint_detail(data_point_id)
    if not detail:
        raise HTTPException(404, "DataPoint not found")
    return detail


@router.get("/consistency")
def consistency(_user: dict = Depends(get_current_user)):
    _demo()
    return {"checks": dpm.run_consistency_checks(), "rules": dpm.VALIDATION_RULES}


@router.get("/facts/m1")
def facts_m1(_user: dict = Depends(get_current_user)):
    """M1 facts enriched with DataPointID + CategorisationKey."""
    _demo()
    return dpm.enriched_m1_facts()
