from datetime import datetime, timedelta

# import OS
import os

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(2),
    "email": ["pierre@restart.us"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    dag_id="pullAppleData",
    default_args=default_args,
    description="Pulling daily Apple data trial",
    schedule_interval=timedelta(days=1),
)


def get_apple_file():
    import requests
    import csv

    url1 = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2012HotfixDev18/v3/en-us/applemobilitytrends-2020-07-18.csv"
    csv_file = open("DownloadedApple.csv", "wb")
    r = requests.get(url1).content
    # print("/n/n" + r[0] + "/n/n")
    csv_file.write(r)
    csv_file.close


task1 = PythonOperator(
    task_id="getCSVfromURL", python_callable=get_apple_file, dag=dag
)

task2 = BashOperator(
    task_id="print_date",
    bash_command="date",
    dag=dag,
)

task1 >> task2
