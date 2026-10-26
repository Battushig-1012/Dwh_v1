"""Production extractors — connect to Core / ERP read-replicas via SQLAlchemy."""

from __future__ import annotations

from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text


def extract_incremental(
    connection_url: str,
    sql: str,
    watermark: datetime | None = None,
) -> pd.DataFrame:
    """
    Incremental load using updated_at / created_at watermark.
    Example sql: SELECT * FROM loans WHERE updated_at > :wm
    """
    engine = create_engine(connection_url)
    params = {"wm": watermark or datetime(1970, 1, 1)}
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn, params=params)
