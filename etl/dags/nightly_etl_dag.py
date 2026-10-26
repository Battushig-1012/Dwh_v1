"""
Apache Airflow DAG — schedule nightly at 02:00 Asia/Ulaanbaatar.
Copy this file into your Airflow dags/ folder when Airflow is deployed.
"""

from __future__ import annotations

from datetime import datetime

try:
    from airflow import DAG
    from airflow.operators.bash import BashOperator

    with DAG(
        dag_id="bbsb_nightly_etl",
        description="BBSB DWH nightly extract → DQ → core → marts",
        schedule="0 2 * * *",
        start_date=datetime(2026, 1, 1),
        catchup=False,
        tags=["bbsb", "dwh", "srep"],
    ) as dag:
        BashOperator(
            task_id="run_nightly_etl",
            bash_command="cd /opt/etl && PYTHONPATH=/opt/etl python -m src.run_nightly",
        )
except ImportError:
    # Airflow not installed in local CLI environment — DAG is documentation + deploy artifact
    dag = None
