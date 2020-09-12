"""Dag for calcat scraping."""
from datetime import datetime, timedelta
from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from airflow.utils.dates import days_ago  # type:ignore
import pandas as pd  # type: ignore

CALCAT_FULL_REF_DATA_URL = "https://raw.githubusercontent.com/StateOfCalifornia/CalCAT/master/data/CA/can_full_reff_table.csv"

dag = DAG(
    dag_id="calcatdatapull",
    description="Daily calCAT data pull",
    schedule_interval=timedelta(minutes=1),
    start_date=datetime(2020, 7, 27),
    catchup=False,
)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["ethan@restart.us"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


def read_url():
    """Pull data from URL into a dataframe and writes to current directory with
    specified filename."""
    URL = "https://raw.githubusercontent.com/StateOfCalifornia/CalCAT/master/data/CA/can_full_reff_table.csv"
    # filename = "calCAT_full_ref.h5"
    filename = "calCAT_full_ref.csv"
    df = pd.read_csv(URL, sep=",")
    # df.to_hdf(filename, key='df', mode='w')
    df.to_csv(filename, mode="w")


pull_task = PythonOperator(
    task_id="calcatpull1", python_callable=read_url, dag=dag
)

date_task = BashOperator(task_id="dateprint", bash_command="date", dag=dag)

date_task >> pull_task
