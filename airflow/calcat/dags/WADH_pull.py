from typing import List
import datetime as dt
import pathlib

import pandas as pd  # type: ignore

from airflow import DAG  # typing: ignore
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
URL: str = "https://www.doh.wa.gov/Portals/1/Documents/1600/coronavirus/data-tables/PUBLIC_CDC_Event_Date_SARS.xlsx"
NAMES: List[str] = [
    "cases_by_age_county",
    "hospitalizations_by_age_county",
    "deaths_by_age_county",
    "datadict",
]
PATH0: pathlib.PosixPath = pathlib.Path("../../extern/data/epidemiological/WA")

# grab, read, and write data
def rw_all(format: str = ".csv"):
    for i in range(4):
        # grab csv from url and convert to dataframe
        df: pd.DataFrame = pd.DataFrame(index=[], columns=[])
        try:
            df = pd.read_excel(URL, sheet_name=i)
        except Exception as e:
            dagmod.bad_url(URL, e)

        # set path and write dataframe in desired format
        path: pathlib.PosixPath = PATH0.joinpath(NAMES[i] + format)
        dagmod.rw(format, path, df)


# define operators and dag
dag: DAG = dagmod.create_dag("WADHdatapull", "weekly WADH data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op("WADHdatapull", rw_all, [], dag)

date_task >> pull_task
