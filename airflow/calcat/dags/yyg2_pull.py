import datetime as dt
import pandas as pd
import pathlib

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
YY_URL: str = "https://raw.githubusercontent.com/youyanggu/covid19_projections/master/projections/combined/latest_subregion.csv"
PATH0: pathlib.PosixPath = pathlib.Path(
    "../../extern/data/epidemiological/us/forecasts/YYG/county"
)
WFORMAT: str = ".csv"
FILENAME: str = "YYG_county_us_casesdeathsprojR"

# build path
path: pathlib.PosixPath = PATH0.joinpath(FILENAME + WFORMAT)

# define operators and dag
dag: DAG = dagmod.create_dag("YYG2datapull", "daily YYG2 data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op(
    "YYG2countypull", dagmod.rw_all, [WFORMAT, [path], [YY_URL]], dag
)

date_task >> pull_task
