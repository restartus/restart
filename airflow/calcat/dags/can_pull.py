"""DAG for pulling COVID Act Now data."""
from pathlib import Path
from typing import List

from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore

import dagmod

# constants
URL0: str = "https://data.covidactnow.org/latest/us/"
URL1: str = ".timeseries.csv"
PATH0: Path = Path("../../extern/data/epidemiological/us/forecasts/CAN")
WFORMAT: str = ".csv"
AGGS: List[str] = ["states", "counties"]
INTERVENTIONS: List[str] = [
    "NO_INTERVENTION",
    "WEAK_INTERVENTION",
    "STRONG_INTERVENTION",
    "OBSERVED_INTERVENTION",
]

# build filepaths and urls for all pairs of agg. and intervention
paths: List[Path] = []
urls: List[Path] = []
for agg in AGGS:
    for intervention in INTERVENTIONS:

        url: Path = Path(URL0 + agg + "." + intervention + URL1)
        urls.append(url)

        filename: str = "can_" + agg + "_" + intervention + WFORMAT
        path: Path = PATH0.joinpath(filename)
        paths.append(path)

# define operators and dag
dag: DAG = dagmod.create_dag("CANdatapull", "Covid act now data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op(
    "CANdatapull", dagmod.rw_all, [WFORMAT, paths, urls], dag
)

date_task >> pull_task
