# dagmod.py
# @author: Ethan Eason
# August 2020

"""
A module containing useful variables and functions for writing
Airflow DAGs that grab CSV formatted data from URLs.
"""

import pathlib
import datetime as dt
from typing import List, Dict

import pandas as pd

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago

# exception for illegal arguments
class IllegalArgumentError(ValueError):
    pass


# prints informative error report message for failed URLs
def bad_url(url: str, e: Exception):

    print("\nProblem found with " + url + " via " + str(e) + "\n")
    print("Check if the datasource's URL has changed.\n")


# global default arguments for instantiating a dag
DEFAULT_ARGS: Dict[str, any] = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "email": ["ethan@restart.us"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": dt.timedelta(minutes=1),
    "catchup": False,
}


# returns a bash operator that prints the date
# <dag> : dag object to assign the date op to
def get_date_op(dag: DAG):

    return BashOperator(task_id="dateprint", bash_command="date", dag=dag)


# returns a python operator
#   str <tid> : task id
#   function <func> : python callable
#   list <funcargs> : ordered args for python callable
def get_pull_op(tid: str, func: callable, funcargs: List[any], dag: DAG):

    return PythonOperator(
        task_id=tid, python_callable=func, op_args=funcargs, dag=dag
    )


# returns a dag object
#   str <did> : dag id
#   str <desc> : dag description
#   datetime.timedelta <freq> : schedule interval
def create_dag(did: str, desc: str, freq: dt.timedelta = dt.timedelta(days=1)):

    return DAG(
        dag_id=did,
        default_args=DEFAULT_ARGS,
        description=desc,
        schedule_interval=freq,
    )


# writes a dataframe to <path> with extension <format>
#   str <format> : file format for writing (either .csv or .h5)
#   posix path <path> : path for writing
#   pandas DataFrame <df> : dataframe to write
def rw(format: str, path: pathlib.posixpath, df: pd.DataFrame):

    if format == ".csv":

        df.to_csv(path, mode="w")

    elif format == ".h5":

        df.to_hdf(path, key=df, mode="w")

    else:

        raise IllegalArgumentError(
            "Must specify either .csv or .h5 as file format."
        )


# returns a dataframe with data grabbed from <url>
#   str <url> : URL to grab csv from
def grab_csv(url: str):

    df: pd.DataFrame = pd.DataFrame()

    try:

        df = pd.read_csv(url)

    except Exception as e:

        bad_url(url, e)

    return df


# grabs data from each url and writes it to its respective path
#   str <format> : file format for writing
#   list of posix paths <paths> : paths for writing
#   list of strs <urls> : urls for grabbing data
def rw_all(format: str, paths: List[pathlib.PosixPath], urls: List[str]):

    for path, url in zip(paths, urls):

        rw(format, path, grab_csv(url))
