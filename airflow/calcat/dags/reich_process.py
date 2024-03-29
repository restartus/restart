"""DAG for processing Reich Lab collected forecast into datacube."""
import pandas as pd
import numpy as np
import pathlib
from typing import List, Dict, Tuple, Optional
import datetime as dt
import h5py

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import dagmod

REICH_PATH: pathlib.PosixPath = pathlib.PosixPath(
    "../../extern/data/covidmodels/covid19-forecast-hub"
)
FORECASTS_PATH: pathlib.PosixPath = REICH_PATH.joinpath("data-processed")
DONT_USE: List[str] = [
    "Karlen-pypm",
    "Imperial-ensemble1",
    "Imperial-ensemble2",
]  # due to licensing
NUM_DATE_CHARS: int = 10
VOLD_DATE: dt.datetime = dt.datetime.strptime("2000-01-01", "%Y-%m-%d")
SUB_THRESHOLD: dt.datetime = dt.datetime.today() - dt.timedelta(weeks=2)
TODAY: pd.Timestamp = pd.to_datetime(
    str(pd.Timestamp.today())[:NUM_DATE_CHARS]
)


def get_file_date(filepathstr: str):
    """Return date file was submitted given string rep. of file's path."""
    # date always follows last / in path
    dateidx: int = filepathstr.rindex("/") + 1
    s: slice = slice(start=dateidx, stop=(dateidx + NUM_DATE_CHARS))
    strdate: str = filepathstr[s]
    return dt.datetime.strptime(strdate, "%Y-%m-%d")


def get_latest_file(paths: List[pathlib.PosixPath]):
    """Return the path to the file with most recent date."""
    # set latest to date far in past, latestpath to
    # empty path for initial loop logic
    latest: dt.datetime = VOLD_DATE
    latestpath: pathlib.PosixPath = pathlib.PosixPath("")

    for path in paths:

        pathdate: dt.datetime = get_file_date(str(path))

        if pathdate > latest:
            latest = pathdate
            latestpath = path

    return latestpath


def get_forecasts():
    """Return dictionary of team-model to forecast filepath."""
    # all forecast files submitted for each team-model are stored in the
    # team-model's directory within the directory at FORECASTS_PATH
    paths: List[pathlib.PosixPath] = [
        path for path in FORECASTS_PATH.iterdir() if "." not in str(path)[-4:]
    ]

    refs: Dict[str, pathlib.PosixPath] = {}
    for path in paths:

        # need team-model name for dict keys
        str_path: str = str(path)
        s: slice = slice(start=str_path.rindex("/") + 1, stop=-1)
        name: str = str_path[s]

        # skip the models we don't want
        if name in DONT_USE:
            continue

        # only want forecast csv files
        files: List[pathlib.PosixPath] = [
            file for file in path.iterdir() if file.suffix == ".csv"
        ]

        # skip to next directory if no files found
        if files == []:
            continue

        # find latest file, and only add if submitted after the
        # submission threshold date (to avoid outdated forecasts)
        latestfile: pathlib.PosixPath = get_latest_file(files)
        if get_file_date(str(latestfile)) > SUB_THRESHOLD:
            refs[name] = latestfile

    return refs


def get_agg(loc: int):
    """Return level of geo aggregation for fips loc."""
    if loc == 0:
        return "country"
    elif loc < 100:
        return "state"
    else:
        return "county"


def get_state(fips: int):
    """Return state of county <fips>."""
    strfips: str = str(fips)

    # add zero so that pattern matching is consistent
    if len(strfips) == 4:
        strfips = "0" + strfips

    # state is always first two digits
    return int(strfips[:2])


def process_file(path: pathlib.PosixPath, name: str):
    """Return processed dataframe built from the forecast file at path."""
    # keep initial types consistent
    df: pd.DataFrame = pd.read_csv(
        path,
        dtype={
            "target": "str",
            "target_end_date": "str",
            "location": "str",
            "type": "str",
            "quantile": "str",
            "value": "float",
        },
    )

    # check if empty
    if len(df) == 0:
        return df

    # encode US as 0 to remedy conflicting location dtypes
    df["location"] = df["location"].replace("US", 0)

    # specified types are needed for indexing later
    df["target_end_date"] = pd.to_datetime(df["target_end_date"])
    df = df.astype(
        {"location": "uint32", "quantile": "float", "value": "uint32"}
    )

    # extract units of target value
    # value_unit_target: what 'value' is a prediction of
    # value_unit_dif: whether 'value' is cumulative or incremental
    # value_unit_type: whether 'value' is a quantile or point prediction
    # value_unit_quantile: quantile value (NA if point)
    def get_slice(target: str):
        return slice(start=(target.rindex(" ") + 1), stop=-1)

    df["value_unit_target"] = df["target"].map(lambda x: x[get_slice(x)] + "s")
    df["value_unit_dif"] = df["target"].map(
        lambda x: "cum" if "cum" in x else "inc"
    )
    df.rename(
        columns={"type": "value_unit_type", "quantile": "value_unit_quantile"},
        inplace=True,
    )

    # no cum or old forecasts
    df = df[
        (df.value_unit_dif != "cum") & (df.target_end_date > TODAY)
    ].reset_index(drop=True)

    # no need for forecast date and target columns after processing
    df.drop(
        columns=["forecast_date", "target", "value_unit_dif"], inplace=True
    )

    # add model identifier column (team-model)
    df["source"] = [name] * len(df)

    # reorder columns in a convenient fashion
    df = df[
        [
            "source",
            "target_end_date",
            "location",
            "value",
            "value_unit_type",
            "value_unit_quantile",
            "value_unit_target",
        ]
    ]

    return df


def build_df():
    """Return dataframe comprised of latest Reich Lab collected forecasts."""
    df: pd.DataFrame = pd.DataFrame(
        {
            "source": pd.Series([], dtype="str"),
            "target_end_date": pd.Series([], dtype="datetime64[ns]"),
            "location": pd.Series([], dtype="uint32"),
            "value": pd.Series([], dtype="uint32"),
            "value_unit_type": pd.Series([], dtype="str"),
            "value_unit_quantile": pd.Series([], dtype="float"),
            "value_unit_target": pd.Series([], dtype="str"),
        }
    )

    # {team-model : filepath}
    modeldict: Dict[str, pathlib.PosixPath] = get_forecasts()

    for name, file in modeldict.items():

        df_from_file = process_file(file, name)

        # no point in concatenating empty dataframe
        if len(df_from_file.index) == 0:
            continue

        df = pd.concat([df, df_from_file], ignore_index=True)

    return df


def build_cube():
    """Return datacube of latest Reich Forecasts.

    Returns 6-dimensional (very sparse) array of most recently
    submitted Reich Lab collected forecasts and respective index labels.

    Each of the cube's dimensions are defined in a way such that
    an index value corresponds to a unique label. For instance,
    the date dimension is defined such that its index values
    0, 1, 2, ..., N correspond to dates d1, d2, d3, ..., dN.

    Some side notes:
    - To remedy point versus quantile predictions, point predictions
    are stored with the quantile index value labelled 0.5. However,
    if a team submits both quantile and point predictions for a common
    target, only the quantile forecast is kept. This way we can use
    the quantile index to index point predictions as well.
    - A state index value of 0 corresponds to country level forecasts,
    a county index value of 0 corresponds to state level forecasts.
    - As documented on the covid19-forecast-hub github repo, case and
    death forecasts are for week totals, whereas hospital forecasts
    are for day totals. The only forecasts for counties are cases.

    Dimensions:
        Date - by date starting on today's (whenever this is run) date.
        State - by 2 digit state fips codes
        County - by 3 digit county fips codes
        Quantile - by quantile value (0.01, 0.025, 0.05, 0.1, 0.15, ...,
                   0.95, 0.975, 0.99)
        Model - by team-model name
        Target - by what a particular forecast is predicting (cases,
                 hospitalizations, deaths)
    """
    df: pd.DataFrame = build_df()

    def date_idx():
        """Return list of dates whose values label the cube's date index."""
        dates = list(set(df["target_end_date"]))
        dates.sort()
        date_index = pd.date_range(start=TODAY, end=dates[-1], freq="D")
        return list(date_index)

    def state_county_idxs():
        """Return lists of states, counties labelling those cube indices."""
        fips = set(df["location"])

        # 0s are for indexing state and country forecasts
        # that is, state level forecasts are stored with a
        # county index value of 0 and country level forecasts
        # are stored with a state index value of 0
        state_index = [0]
        county_index = [0]

        for loc in fips:

            fips_len = len(str(loc))

            # state fips always only 1 or 2 digits
            if fips_len <= 2 and loc != 0:
                state_index.append(loc)

            # county fips always more than 2 digits
            elif fips_len > 2:
                county_index.append(int(str(loc)[-3:]))

        # sort so that indices have logical ordering
        state_index.sort()
        county_index = list(set(county_index))
        county_index.sort()

        return state_index, county_index

    def quantile_idx():
        """Return list of quantiles labelling the cube's quantile index."""
        return (
            [0.01, 0.025]
            + [round(val, 2) for val in np.arange(0.05, 1.0, 0.05)]
            + [0.975, 0.99]
        )

    def model_idx():
        """Return list of names labelling the cube's model index."""
        models = list(set(df["source"]))
        models.sort()
        return models

    # need to build all index labels
    date_index = date_idx()
    state_index, county_index = state_county_idxs()
    quantile_index = quantile_idx()
    model_index = model_idx()
    target_index = ["cases", "hosps", "deaths"]

    def get_state_county_idx(loc):
        """Return state and county cube index values for loc."""
        loc_str: str = str(loc)

        # if loc is a state, county index is 0
        if len(loc_str) <= 2:
            return state_index.index(loc), 0

        state: int = get_state(loc)
        s: slice = slice(start=len(str(state)), stop=-1)
        county = int(loc_str[s])

        return state_index.index(state), county_index.index(county)

    # need to encode colomn labels as index values
    # so that corresponding values can be retrieved
    # from each tuple generated by df.itertuples() (in
    # the for loop ~30 lines below) and used by get_indices.
    src: int = 0  # 'source'
    ted: int = 1  # 'target_end_date'
    loc: int = 2  # 'location'
    val: int = 3  # 'value'
    vut: int = 4  # 'value_unit_type'
    vuq: int = 5  # 'value_unit_quantile'
    vuta: int = 6  # 'value_unit_target'

    def get_indices(row):
        """Return a tuple of index values for the given df row's value."""
        # we don't want cumulative, nor old forecasts
        if row[ted] < TODAY:
            return

        date_idx: int = date_index.index(row[ted])
        state_idx: Optional[int] = None
        county_idx: Optional[int] = None
        state_idx, county_idx = get_state_county_idx(row[loc])

        # for point predictions, we just set the quantile to 0.5
        quantile_val: float = 0.5
        if row[vut] == "quantile":
            quantile_val = row[vuq]

        quantile_idx: int = quantile_index.index(quantile_val)
        model_idx: int = model_index.index(row[src])
        target_idx: int = target_index.index(row[vuta])

        return (
            date_idx,
            state_idx,
            county_idx,
            quantile_idx,
            model_idx,
            target_idx,
        )

    cube = np.zeros(
        shape=(
            len(date_index),
            len(state_index),
            len(county_index),
            len(quantile_index),
            len(model_index),
            len(target_index),
        ),
        dtype=int,
    )

    for row in df.itertuples(index=False):

        index: Tuple[int, int, int, int, int, int] = get_indices(row)

        if index is None:
            continue

        value: int = row[val]
        if value == 0:
            # true 0s encoded as -1 for sparse rep
            # this is reversed on the other end
            value = -1

        # in the case that a quantile prediction value has already
        # been added to the cube at index for 0.5 quantile, we
        # ignore the point prediction. otherwise we add the point
        # prediction at the 0.5 quantile index value. This point
        # value will get overridden if a value for the 0.5 quantile
        # is later found.
        if row[vut] == "point" and cube[index] != 0:
            continue

        cube[index] = value

    index = {
        "date_index": date_index,
        "state_index": state_index,
        "county_index": county_index,
        "quantile_index": quantile_index,
        "model_index": model_index,
        "target_index": target_index,
    }

    return cube, index


def produce_cube():
    """Build and save data cube of Reich lab collected forecasts and its indices.

    Cube (ndarray), indices (dataframe) are saved as hdf5, csv respectively.
    """
    cube, index = build_cube()

    # write cube to disk with gzip compression as cube is sparse and large
    with h5py.File(
        "../../extern/data/epidemiological/processed/reich.hdf5", "w"
    ) as cube_file:
        cube_file.create_dataset(
            "zipped_reichcube", data=cube, compression="gzip"
        )

    # write indices to dataframe as csv for simplicity
    dfindex = pd.DataFrame()
    dflen = max(cube.shape)
    for key, val in index.items():
        # need consistent column lengths
        dfindex[key] = val + ([None] * (dflen - len(val)))
    dfindex.to_csv(
        "../../extern/data/epidemiological/processed/reichindex.csv"
    )


desc = (
    "Processes latest Reich Lab collected forecasts and builds"
    + "datacube and indices."
)
dag: DAG = dagmod.create_dag("ReichLabDataCube", desc)
date_task: BashOperator = dagmod.get_date_op(dag)
cube_task: PythonOperator = PythonOperator(
    task_id="ReichCube", python_callable=produce_cube, dag=dag
)

date_task >> cube_task
