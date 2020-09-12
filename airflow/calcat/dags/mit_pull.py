"""Pull MIT Data."""
from typing import List, Dict
import datetime as dt

import pandas as pd  # type:ignore
from airflow import DAG  # type:ignore
from airflow.operators.bash_operator import BashOperator  # type:ignore
from airflow.operators.python_operator import PythonOperator  # type:ignore
from airflow.utils.dates import days_ago  # type:ignore

import dagmod

# constants
URL: str = "https://raw.githubusercontent.com/COVIDAnalytics/website/master/data/predicted/Global.csv"
PATH0: str = "../../extern/data/epidemiological/us/forecasts/MIT/"
YESTERDAY: str = (dt.datetime.now() - dt.timedelta(days=1)).strftime(
    "%Y-%m-%d"
)
STATES: Dict[str, str] = {
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

# returns list of str paths corresponding to agg and location specified
def build_paths(agg: str, loc: str):

    # prepare filename and inital path
    filename: str = "MIT_" + agg + "_" + STATES[loc] + "_"
    path0: str = PATH0 + agg

    # create path for cases, deaths, and R-value data
    paths: List[str] = [path0 for i in range(3)]
    paths[0] += "/cases/" + filename + "casesproj"
    paths[1] += "/deaths/" + filename + "deathsproj"
    paths[2] += "/hospital/" + filename + "hospitalproj"

    return paths


# grab, read, and write all data
def rw_cases_deaths_hosp(url: str, format: str = ".csv"):

    # check arg format
    if not format in [".csv", ".h5"]:
        raise dagmod.IllegalArgumentError(
            "Must specify either .csv" + "or .h5 as file format."
        )

    # grab data from url
    df: pd.DataFrame = dagmod.grab_csv(url)

    # seggregate data and write for each state
    df = df.loc[df["Country"] == "US"]
    for state in STATES.keys():

        # filter for current state
        dfs: pd.DataFrame = df[df["Province"] == state]

        # collect cases, deaths, and hospital into separate dataframes
        cases, deaths, hospital = (
            dfs.filter(
                regex="Detected$|Active$|Day|Province", axis=1
            ).reset_index(drop=True),
            dfs.filter(regex="Deaths|Day|Province", axis=1).reset_index(
                drop=True
            ),
            dfs.filter(
                regex="Hospitalized|Ventilated|Day|Province", axis=1
            ).reset_index(drop=True),
        )

        # build paths for writing
        paths: List[str] = build_paths("state", state)

        # write data
        paths = [path + format for path in paths]
        if format == ".csv":
            cases.to_csv(paths[0], mode="w")
            deaths.to_csv(paths[1], mode="w")
            hospital.to_csv(paths[2], mode="w")
        else:  # only other format is .h5
            cases.to_hdf(paths[0], key="df", mode="w")
            deaths.to_hdf(paths[1], key="df", mode="w")
            hospital.to_hdf(paths[2], key="df", mode="w")


# callable for python op
def pull_mit():
    rw_cases_deaths_hosp(URL)


# define operators and dag
dag: DAG = dagmod.create_dag("MITdatapull", "daily MIT data pull (states)")

pull_states_task: PythonOperator = dagmod.get_pull_op(
    "MITstatespull", pull_mit, [], dag
)

date_task: BashOperator = dagmod.get_date_op(dag)

date_task >> pull_states_task
