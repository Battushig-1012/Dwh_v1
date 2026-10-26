from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import demo_data
from ..auth.deps import get_current_user
from ..config import settings
from ..db import get_db

router = APIRouter()


@router.get("")
def list_dictionary(
    schema: str | None = Query(None),
    table: str | None = Query(None),
    db: Session | None = Depends(get_db),
    _user: dict = Depends(get_current_user),
):
    if settings.demo_mode:
        rows = demo_data.DICTIONARY
        if schema:
            rows = [r for r in rows if r["schema_name"] == schema]
        if table:
            rows = [r for r in rows if r["table_name"] == table]
        return rows

    assert db is not None
    sql = """
        SELECT dict_id, schema_name, table_name, column_name,
               business_name_mn, business_name_en, description_mn, description_en,
               data_type, unit_of_measure, is_pii, is_mandatory,
               data_owner, data_steward, classification
        FROM governance.data_dictionary
        WHERE (:schema IS NULL OR schema_name = :schema)
          AND (:table IS NULL OR table_name = :table)
        ORDER BY schema_name, table_name, column_name
    """
    rows = db.execute(text(sql), {"schema": schema, "table": table}).mappings().all()
    return [dict(r) for r in rows]
