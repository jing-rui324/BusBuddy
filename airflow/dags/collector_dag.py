from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="bus_arrival_collector",
    start_date=datetime(2026, 10, 23),
    schedule="@hourly",
    catchup=False,
    tags=["busbuddy"],
) as dag:
    collect_bus_arrivals = BashOperator(
        task_id="collect_bus_arrivals",
        bash_command="cd /opt/busbuddy && python -m src.ingestion",
        retries=2,
        retry_delay=timedelta(minutes=5),
    )