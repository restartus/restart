"""DAG for pulling the UW state policy data."""
import pathlib

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
UWP_URL: str = "https://query.data.world/s/vfpfdftmwmk3qj7fbobnrpas5kxuj2"
PATH0: pathlib.PosixPath = pathlib.PosixPath(
    "../../extern/data/epidemiological/us/policy"
)
WFORMAT: str = ".csv"
FILENAME: str = "UW_state_us_policy"

# build path
path: pathlib.PosixPath = PATH0.joinpath(FILENAME + WFORMAT)

# define operators and dag
dag: DAG = dagmod.create_dag("UWPdatapull", "daily UW policy data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op(
    "UWpolicypull", dagmod.rw_all, [WFORMAT, [path], [UWP_URL]], dag=dag
)

date_task >> pull_task
