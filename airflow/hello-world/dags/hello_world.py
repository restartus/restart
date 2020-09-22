"""Create a Hello World Demo."""
from datetime import datetime
from airflow import DAG  # type:ignore
from airflow.operators.dummy_operator import DummyOperator  # type:ignore
from airflow.operators.python_operator import PythonOperator  # type:ignore


def print_hello():
    """Say Hello World."""
    return "hello world"


dag = DAG(
    "hello_world",
    description="Hello World DAG",
    schedule_interval="0 12 * * *",
    start_date=datetime(2020, 6, 1),
    catchup=False,
)

dummy_op = DummyOperator(task_id="dummy_task", retries=3, dag=dag)

hello_op = PythonOperator(
    task_id="hello_task", python_callable=print_hello, dag=dag
)

dummy_op >> hello_op
