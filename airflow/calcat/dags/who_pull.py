"""DAG for pulling WHO Covid data."""
import pathlib

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
WHO_URL: str = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
PATH0: pathlib.PosixPath = pathlib.PosixPath(
    "../../extern/data/epidemiological/global"
)
WFORMAT: str = ".csv"
FILENAME: str = "WHO-COVID-19-global-data"

# build path
path: pathlib.PosixPath = PATH0.joinpath(FILENAME + WFORMAT)

# define operators and dag
dag: DAG = dagmod.create_dag("WHOdatapull", "daily WHO data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op(
    "WHOdatapull", dagmod.rw_all, [WFORMAT, [path], [WHO_URL]], dag
)

date_task >> pull_task
