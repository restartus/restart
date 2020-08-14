"""Utilities.

Main utilities
"""
import datetime
import os
from pathlib import Path
from typing import Dict, Optional, Union

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore


def set_config(path: str):
    """Set a confuse configuration."""
    os.environ["CONFIGDIR"] = os.path.abspath(path)
    config = confuse.Configuration("config")
    return config


def is_dir_or_file(name: str) -> bool:
    """Is path a directory or a file.

    It's hard to believe this is not a function already
    """
    path = Path(name)
    if path.is_dir() or path.is_file():
        return True
    return False


# sets the frame properly but does need to understand the model
# so goes into the model method
def set_dataframe(
    arr: np.ndarray,
    label: Optional[Dict],
    index: Optional[str] = None,
    columns: Optional[str] = None,
) -> pd.DataFrame:
    """Set the dataframe up.

    Using the model data Dictionary and labels
    """
    # we use get so that if there is no item it returns None
    # https://www.tutorialspoint.com/python/dictionary_get.htm
    df = pd.DataFrame(
        arr,
        index=label[index]
        if label is not None and index is not None
        else None,
        columns=label[columns]
        if label is not None and columns is not None
        else None,
    )
    df.index.name = index
    df.columns.name = columns
    return df


def load_dataframe(fname: str) -> pd.DataFrame:
    """Load h5 file into a dataframe.

    Args:
        Name of h5 file

    Returns:
        The dataframe serialized in the h5 file
    """
    df: pd.DataFrame = pd.read_hdf(fname, "df")
    return df


def datetime_to_code(code: Union[str, datetime.datetime]) -> str:
    """Convert datetime objects to valid OCC codes.

    Gets around the problem of Excel automatically converting date-looking
    strings into datetime objects that can't be undone.

    Args:
        code: Either a datetime object or string represnting an OCC code

    Returns:
        The code in valid OCC code format
    """
    if type(code) is datetime.datetime:
        return str(code.month) + "-" + str(code.year)  # type: ignore
    else:
        return str(code)
