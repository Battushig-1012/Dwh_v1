from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import demo_data
from ..auth.deps import get_current_user
from ..config import settings
from ..db import get_db

router = APIRouter()


@router.get("/batches")
def recent_batches(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.BATCHES
    assert db is not None
    rows = db.execute(
        text(
            """
            SELECT batch_id, dag_run_id, started_at, finished_at, status,
                   source_systems, rows_extracted, rows_loaded_core, rows_rejected, error_message
            FROM staging.etl_batch_log
            ORDER BY started_at DESC
            LIMIT 20
            """
        )
    ).mappings().all()
    return [dict(r) for r in rows]


@router.get("/results")
def dq_results(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.DQ_RESULTS
    assert db is not None
    rows = db.execute(
        text(
            """
            SELECT result_id, batch_id, rule_code, rule_name, target_table,
                   severity, passed, failed_rows, total_rows, details, checked_at
            FROM governance.dq_rule_results
            ORDER BY checked_at DESC
            LIMIT 100
            """
        )
    ).mappings().all()
    return [dict(r) for r in rows]


@router.get("/audit")
def audit_trail(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return demo_data.AUDIT
    assert db is not None
    rows = db.execute(
        text(
            """
            SELECT audit_id, event_time, actor, action, entity_type, entity_id, after_state
            FROM governance.audit_trail
            ORDER BY event_time DESC
            LIMIT 100
            """
        )
    ).mappings().all()
    return [dict(r) for r in rows]
