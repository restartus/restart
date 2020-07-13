import math
import datetime
import yaml
import numpy as np
import pandas as pd
from typing import Union, Dict


def datetime_to_code(code: Union[str, datetime.datetime]) -> str:
    """Converts datetime objects to valid OCC codes

    It's very dumb that this even needs to be a thing but since Excel
    automatically converts numbers that *might* be interpreted as dates
    into dates, and there's no way to have it not do this, we need a way
    to turn datetime objects into OCC codes.

    Args:
        code: Either a datetime object or a string that represents an OCC code

    Returns:
        The code in valid OCC code format
    """
    if type(code) is datetime.datetime:
        return str(code.month) + '-' + str(code.year)
    else:
        return code


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    """Manually slice the excel model to get the data we need.

    Args:
        df: The excel model loaded into a dataframe

    Returns:
        Slice dataframe
    """
    # manually redo indexing and select rows we need
    df.columns = df.iloc[2528]
    df = df.iloc[2529:3303]
    df = df[['Washington SOT', 'SOC', 'Type', 'Level']]

    # fix datetime objects and drop empty rows
    df['SOC'] = df['SOC'].apply(datetime_to_code)
    df = df.dropna(axis='rows')

    return df


def health_df(df: pd.DataFrame) -> pd.DataFrame:
    """Slice the dataframe so it's just healthcare workers.

    Args:
        df: Dataframe that has been formatted with format_df()

    Returns:
        The sliced dataframe

    """
    return df[(df['SOC'].str.startswith('29-')) |
              (df['SOC'].str.startswith('31-'))]


def gen_mappings(df: pd.DataFrame) -> Dict:
    """Generate mappings for OCC codes and population levels.

    Args:
        df: The excel model that has been processed and sliced

    Returns:
        Dictionary of the population level mappings
    """
    mapping = {}

    for i in range(df.shape[0]):
        arr = np.zeros(7)
        level = df.iloc[i]['Level']

        # assign integer levels
        if type(level) is int:
            arr[level] = 1

        # assign multiple levels
        else:
            arr[math.floor(level)] = 0.5
            arr[math.ceil(level)] = 0.5

        # add to dictionary
        mapping[df.iloc[i]['Washington SOT']] = arr.tolist()

    return mapping


def save_dict(df, fname):
    """Save mappings to a yaml file.

    Args:
        df: The excel model that has been processed and sliced
        fname: What we want to name the yaml file

    Returns:
        None
    """
    # generating the map dictionary
    mapping = gen_mappings(df)

    # dump into yaml
    with open(fname, 'w') as yaml_file:
        yaml.dump({"Map": mapping}, yaml_file, default_flow_style=None)

    return None


if __name__ == '__main__':
    df = pd.read_excel('../../../covid-surge-who.xlsx')
    df = health_df(format_df(df))
    save_dict(df, '../california/levels.yaml')
