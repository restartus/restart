"""DAG for pulling YYG state and us data."""
from typing import List
import datetime as dt

import pandas as pd

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
YESTERDAY: str = (dt.datetime.now() - dt.timedelta(days=1)).strftime(
    "%Y-%m-%d"
)
STATES: List[str] = [
    "TX",
    "FL",
    "CA",
    "AZ",
    "SC",
    "GA",
    "AL",
    "LA",
    "OH",
    "NC",
    "MS",
    "TN",
    "NY",
    "IL",
    "PA",
    "IN",
    "NV",
    "NJ",
    "MD",
    "MO",
    "MA",
    "AR",
    "VA",
    "KY",
    "WI",
    "OK",
    "CO",
    "IA",
    "MN",
    "NM",
    "UT",
    "WA",
    "OR",
    "MI",
    "ID",
    "PR",
    "KS",
    "NE",
    "CT",
    "RI",
    "MT",
    "NH",
    "SD",
    "DE",
    "ND",
    "DC",
    "WV",
    "AK",
    "ME",
    "HI",
    "WY",
    "VT",
    "VI",
    "GU",
    "MP",
    "AS",
]
YY_URL: str = (
    "https://raw.githubusercontent.com/youyanggu/"
    + "covid19_projections/master/projections/"
    + YESTERDAY
)


def build_paths(agg: str, loc: str):
    """Return list of paths for agg and loc."""
    # prepare filename and inital path
    filename: str = "YYG_" + agg + "_" + loc + "_"
    path0: str = "../../extern/data/epidemiological/us/forecasts/YYG/" + agg

    # create path for cases, deaths, and R-value data
    paths: List[str] = [path0 for i in range(3)]
    paths[0] += "/cases/" + filename + "casesproj"
    paths[1] += "/deaths/" + filename + "deathsproj"
    paths[2] += "/R/" + filename + "Rvalmean"
    return paths


def rw_cases_deaths_R(url: str, paths: List[str], format: str = ".csv"):
    """Grab, read, and write all data."""
    # check arg format
    if format not in [".csv", ".h5"]:
        raise dagmod.IllegalArgumentError(
            "Must specify either .csv " + "or .h5 as file format."
        )

    # grab data from url
    df: pd.DataFrame = pd.DataFrame(index=[], columns=[])
    try:
        df = pd.read_csv(url)
    except Exception as e:
        dagmod.bad_url(url, e)
        return

    # seggregate data
    cases: pd.DataFrame = pd.DataFrame()
    deaths: pd.DataFrame = pd.DataFrame()
    r: pd.DataFrame = pd.DataFrame()
    cases, deaths, r = (
        df.filter(regex="infected|date", axis=1),
        df.filter(regex="deaths|date", axis=1),
        df.filter(regex="values|date", axis=1),
    )

    # write data
    paths = [path + format for path in paths]
    if format == ".csv":
        cases.to_csv(paths[0], mode="w")
        deaths.to_csv(paths[1], mode="w")
        r.to_csv(paths[2], mode="w")
    else:  # only other format is .h5
        cases.to_hdf(paths[0], key="df", mode="w")
        deaths.to_hdf(paths[1], key="df", mode="w")
        r.to_hdf(paths[2], key="df", mode="w")


def pull_state(state: str):
    """Pull state data."""
    # prepare data url and filepaths
    url: str = YY_URL + "/US_" + state + ".csv"
    paths: List[str] = build_paths(agg="state", loc=state)

    # grab data and write to files
    rw_cases_deaths_R(url, paths, format=".csv")


def pull_us():
    """Pull country data."""
    # prepare data url and filepaths
    url: str = YY_URL + "/US.csv"
    paths: List[str] = build_paths(agg="country", loc="US")

    # grab data and write to files
    rw_cases_deaths_R(url, paths, format=".csv")


def pull_states():
    """Pull all states data."""
    # states data
    for state in STATES:
        pull_state(state)


# define operators and dag
dag: DAG = dagmod.create_dag(
    "YYGdatapull", "daily YYG data pull (states + us)"
)

pull_states_task: PythonOperator = dagmod.get_pull_op(
    "YYGstatespull", pull_states, [], dag
)

pull_us_task: PythonOperator = dagmod.get_pull_op(
    "YYGuspull", pull_us, [], dag
)

date_task: BashOperator = dagmod.get_date_op(dag)

date_task >> pull_us_task >> pull_states_task
