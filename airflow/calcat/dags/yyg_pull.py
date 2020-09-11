from typing import List
import datetime as dt
import pathlib

import pandas as pd

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

# constants
YESTERDAY = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
STATES = [
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
YY_URL = (
    "https://raw.githubusercontent.com/youyanggu/covid19_projections/master/projections/"
    + YESTERDAY
)


def build_paths(agg: str, loc: str):

    # prepare filename and inital path
    filename = "YYG_" + agg + "_" + loc + "_"
    path0 = "../../extern/data/epidemiological/us/forecasts/YYG/" + agg

    # create path for cases, deaths, and R-value data
    paths = [path0 for i in range(3)]
    paths[0] += "/cases/" + filename + "casesproj"
    paths[1] += "/deaths/" + filename + "deathsproj"
    paths[2] += "/R/" + filename + "Rvalmean"
    return paths


# grab, read, and write all data
def rw_cases_deaths_R(url: str, paths: List[str], format: str = ".csv"):

    # check arg format
    if not format in [".csv", ".h5"]:
        raise dagmod.IllegalArgumentError(
            "Must specify either .csv " + "or .h5 as file format."
        )

    # grab data from url
    df = pd.DataFrame(index=[], columns=[])
    try:
        df = pd.read_csv(url)
    except Exception as e:
        dagmod.bad_url(url, e)
        return

    # seggregate data
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

    # prepare data url and filepaths
    url = YY_URL + "/US_" + state + ".csv"
    paths = build_paths(agg="state", loc=state)

    # grab data and write to files
    rw_cases_deaths_R(url, paths, format=".csv")


def pull_us():
    # prepare data url and filepaths
    url = YY_URL + "/US.csv"
    paths = build_paths(agg="country", loc="US")

    # grab data and write to files
    rw_cases_deaths_R(url, paths, format=".csv")


def pull_states():
    # states data
    for state in STATES:
        pull_state(state)


# define operators and dag
dag = dagmod.create_dag("YYGdatapull", "daily YYG data pull (states + us)")

pull_states_task = dagmod.get_pull_op("YYGstatespull", pull_states, [], dag)

pull_us_task = dagmod.get_pull_op("YYGuspull", pull_us, [], dag)

date_task = dagmod.get_date_op(dag)

date_task >> pull_us_task >> pull_states_task
