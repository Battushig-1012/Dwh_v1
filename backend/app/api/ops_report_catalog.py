"""Unified API for operational / source reports (PRPT, interim, Core calcs)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from ..auth.deps import get_current_user
from ..config import settings
from .. import ops_reports as packs

router = APIRouter()


def _demo():
    if not settings.demo_mode:
        raise HTTPException(501, "Ops reports currently available in DEMO_MODE")


def _spec(code: str):
    spec = packs.get(code)
    if not spec:
        raise HTTPException(404, f"Unknown ops report: {code}")
    return spec


@router.get("")
@router.get("/")
def list_catalog(
    category: str | None = Query(None),
    _user: dict = Depends(get_current_user),
):
    _demo()
    return packs.catalog(category=category)


@router.get("/{code}")
def report_meta(code: str, _user: dict = Depends(get_current_user)):
    _demo()
    spec = _spec(code)
    item = spec.catalog_item()
    item["extra"] = spec.extra
    return item


@router.get("/{code}/overview")
def overview(code: str, _user: dict = Depends(get_current_user)):
    _demo()
    spec = _spec(code)
    if not spec.overview_fn:
        raise HTTPException(501, "overview not implemented for this report")
    return spec.overview_fn()


@router.get("/{code}/pipeline")
def pipeline(code: str, _user: dict = Depends(get_current_user)):
    _demo()
    spec = _spec(code)
    if not spec.pipeline_fn:
        raise HTTPException(501, "pipeline not implemented")
    return spec.pipeline_fn()


@router.get("/{code}/staging")
def staging(code: str, _user: dict = Depends(get_current_user)):
    _demo()
    spec = _spec(code)
    if not spec.staging_fn:
        raise HTTPException(501, "staging not implemented")
    return spec.staging_fn()


@router.get("/{code}/mart")
def mart(
    code: str,
    bal_type: str | None = Query(None),
    chart_code: str | None = Query(None),
    _user: dict = Depends(get_current_user),
):
    _demo()
    spec = _spec(code)
    if not spec.mart_fn:
        raise HTTPException(501, "mart not implemented")
    # Packs may ignore unknown kwargs
    try:
        return spec.mart_fn(bal_type=bal_type, chart_code=chart_code)
    except TypeError:
        return spec.mart_fn()


@router.get("/{code}/sql")
def sql_ref(code: str, _user: dict = Depends(get_current_user)):
    _demo()
    spec = _spec(code)
    if not spec.sql_fn:
        raise HTTPException(501, "sql reference not implemented")
    return spec.sql_fn()
