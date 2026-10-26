from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .. import demo_data
from ..auth.deps import get_current_user
from ..config import settings
from ..db import get_db

router = APIRouter()


@router.get("/graph")
def lineage_graph(db: Session | None = Depends(get_db), _user: dict = Depends(get_current_user)):
    if settings.demo_mode:
        return {"nodes": demo_data.LINEAGE_NODES, "edges": demo_data.LINEAGE_EDGES}

    assert db is not None
    nodes = db.execute(
        text(
            """
            SELECT node_id AS id, node_type AS type, display_name AS label,
                   schema_name, table_name, system_name, description
            FROM governance.lineage_nodes
            """
        )
    ).mappings().all()
    edges = db.execute(
        text(
            """
            SELECT edge_id, from_node_id AS source, to_node_id AS target,
                   transform_type, transform_logic
            FROM governance.lineage_edges
            """
        )
    ).mappings().all()
    return {"nodes": [dict(n) for n in nodes], "edges": [dict(e) for e in edges]}
