# dagmod.py
# @author: Ethan Eason
# August 2020

"""
A module containing useful variables and functions for writing.

Airflow DAGs that grab CSV formatted data from URLs.
"""

from pathlib import Path
import datetime as dt
from typing import List, Dict, Any, Callable

import pandas as pd  # type:ignore

from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from airflow.utils.dates import days_ago  # type: ignore


# exception for illegal arguments
class IllegalArgumentError(ValueError):
    """Illegal argument is ignored for now."""

    pass


def bad_url(url: str, e: Exception):
    """Print informative error report message for failed URLs."""
    print("\nProblem found with " + url + " via " + str(e) + "\n")
    print("Check if the datasource's URL has changed.\n")


# global default arguments for instantiating a dag
DEFAULT_ARGS: Dict[str, Any] = {
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


def get_date_op(dag: DAG):
    """Return a bash operator that prints the date.

    <dag> : dag object to assign the date op to
    """
    return BashOperator(task_id="dateprint", bash_command="date", dag=dag)


def get_pull_op(tid: str, func: Callable, funcargs: List[Any], dag: DAG):
    """Return a python operator.

    #   str <tid> : task id
    #   function <func> : python callable
    #   list <funcargs> : ordered args for python callable
    """
    return PythonOperator(
        task_id=tid, python_callable=func, op_args=funcargs, dag=dag
    )


def create_dag(did: str, desc: str, freq: dt.timedelta = dt.timedelta(days=1)):
    """Create a DAG.

    # returns a dag object
    #   str <did> : dag id
    #   str <desc> : dag description
    #   datetime.timedelta <freq> : schedule interval
    """
    return DAG(
        dag_id=did,
        default_args=DEFAULT_ARGS,
        description=desc,
        schedule_interval=freq,
    )


def rw(format: str, path: Path, df: pd.DataFrame):
    """Write a dataframe to <path> with extension <format>.
    #   str <format> : file format for writing (either .csv or .h5)
    #   posix path <path> : path for writing
    #   pandas DataFrame <df> : dataframe to write
    """
    if format == ".csv":

        df.to_csv(path, mode="w")

    elif format == ".h5":

        df.to_hdf(path, key=df, mode="w")

    else:

        raise IllegalArgumentError(
            "Must specify either .csv or .h5 as file format."
        )


def grab_csv(url: str):
    """Return a dataframe with data grabbed from <url>.

    #   str <url> : URL to grab csv from
    """
    df: pd.DataFrame = pd.DataFrame()

    try:

        df = pd.read_csv(url)

    except Exception as e:

        bad_url(url, e)

    return df


def rw_all(format: str, paths: List[Path], urls: List[str]):
    """Grab data from each url and writes it to its respective path.

    #   str <format> : file format for writing
    #   list of posix paths <paths> : paths for writing
    #   list of strs <urls> : urls for grabbing data
    """
    for path, url in zip(paths, urls):

        rw(format, path, grab_csv(url))
