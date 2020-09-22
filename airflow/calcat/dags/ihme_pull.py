"""DAG for pulling IMHE Data."""
from zipfile import ZipFile
from typing import List
from pathlib import Path
import requests
import io

import pandas as pd  # type: ignore

from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type:ignore

import dagmod

URL: str = (
    "https://ihmecovid19storage.blob.core.windows.net/latest/ihme-covid19.zip"
)
PATH0: Path = Path("../../extern/data/epidemiological/global/IHME")

paths: List[Path] = []


def rw_zip(format: str = ".csv"):
    """Read and write data from zip url to file."""
    if format not in [".csv", ".h5"]:
        raise dagmod.IllegalArgumentError(
            "Must specify either .csv or .h5 as file format."
        )

    # retrieve contents
    try:
        c: requests.Response = requests.get(URL)
    except Exception as e:
        dagmod.bad_url(URL, e)

    # if contents don't checkout, don't proceed and report error
    if not c.ok:
        print(
            "There was a problem with the retrieved content."
            + "Nothing written. Exiting."
        )
        return

    # interpret url contents as zip
    z: ZipFile = ZipFile(io.BytesIO(c.content))

    # check the zipfile
    if z.testzip() is not None:
        print(
            "There was a problem with the zip file."
            + "Nothing written. Exiting."
        )
        return

    # write each csv to /IHME dir in the desired format
    for member in z.namelist():

        # skip if member file is not a csv
        if ".csv" not in member:
            continue

        with z.open(member) as file:

            # read in data
            df = pd.DataFrame()
            try:
                df = pd.read_csv(file)
            except Exception as e:
                print("Exception" + str(e) + " with file " + str(member))

            # build path and write file in desired format
            s: slice = slice(start=member.index("/") + 1, stop=-1)
            path: Path = PATH0.joinpath(member[s])
            dagmod.rw(format, path, df)


dag: DAG = dagmod.create_dag("IHMEdatapull", "daily IHME data pull")

date_task: BashOperator = dagmod.get_date_op(dag)

pull_task: PythonOperator = dagmod.get_pull_op("IHMEallpull", rw_zip, [], dag)

date_task >> pull_task
