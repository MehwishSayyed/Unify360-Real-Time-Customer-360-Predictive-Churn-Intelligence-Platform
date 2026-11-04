"""Smoke test: proves Airflow can reach the warehouse and the schemas exist."""
from datetime import datetime

import psycopg2
from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.operators.python import PythonOperator

EXPECTED_SCHEMAS = {"raw", "staging", "marts", "activation"}


def check_warehouse():
    conn_info = BaseHook.get_connection("warehouse")
    conn = psycopg2.connect(
        host=conn_info.host,
        port=conn_info.port,
        user=conn_info.login,
        password=conn_info.password,
        dbname=conn_info.schema,
    )
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT schema_name FROM information_schema.schemata")
            found = {row[0] for row in cur.fetchall()}
    finally:
        conn.close()

    missing = EXPECTED_SCHEMAS - found
    if missing:
        raise RuntimeError(f"Missing schemas in warehouse: {sorted(missing)}")
    print(f"OK: all schemas present: {sorted(EXPECTED_SCHEMAS)}")


with DAG(
    dag_id="smoke_test",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    tags=["infra"],
) as dag:
    PythonOperator(task_id="check_warehouse", python_callable=check_warehouse)
