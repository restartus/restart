import datetime as dt
import pathlib

import pandas as pd

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
YU_URL: str = "https://docs.google.com/spreadsheets/d/1ZSG7o4cV-G0Zg3wlgJpB2Zvg-vEN1i_76n2I-djL0Dk/export?format=csv&id"
PATH0: pathlib.PosixPath = pathlib.Path(
    "../../extern/data/epidemiological/us/forecasts/Yu/county"
)
FILENAME: str = "YU_county_us_deathsproj"

# grab, read, and write data
def rw_all(format: str = ".csv"):

    # grab csv from url and convert to dataframe
    df: pd.DataFrame() = pd.DataFrame(index=[], columns=[])
    try:
        df = pd.read_csv(YU_URL, header=2)
    except Exception as e:
        dagmod.bad_url(YU_URL, e)

    # set path and write dataframe in desired format
    path = PATH0.joinpath(FILENAME + format)
    dagmod.rw(format, path, df)


# define operators and dag
dag: DAG = dagmod.create_dag("YUdatapull", "daily Yu Group data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op(
    "YUcountypull", rw_all, [], dag=dag
)

date_task >> pull_task
