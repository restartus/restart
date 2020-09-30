"""Utilities.

Main utilities
"""
import datetime
import math
import os
from pathlib import Path
from typing import Dict, Optional, Union

import bqplot  # type: ignore
import confuse  # type: ignore
import ipysheet  # type: ignore
import ipywidgets as widgets  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from bqplot import pyplot as plt  # type: ignore
from IPython.display import display  # type: ignore

chart_colors = [
    "#77AADD",
    "#99DDFF",
    "#44BB99",
    "#BBCC33",
    "#AAAA00",
    "#EEDD88",
    "#EE8866",
    "#FFAABB",
    "#DDDDDD",
    "#000000",
]


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


def to_df(sheet):
    """Shorter function call for sheet -> df."""
    return ipysheet.pandas_loader.to_dataframe(sheet)


def to_sheet(df):
    """Shorter function call for df -> sheet."""
    return ipysheet.pandas_loader.from_dataframe(df)


def format_cells(sheet, money=False):
    """Format ipysheet cells with specific attributes."""
    for cell in sheet.cells:
        setattr(cell, "read_only", True)
        if money is True:
            setattr(cell, "numeric_format", "$0,000")
        else:
            setattr(cell, "numeric_format", "0,000")


def format_population(sheet, money=False, round=False):
    """Generate a formatted sheet optimized for displaying population."""
    df = to_df(sheet)
    if round:
        df = df.round()
    index_name = "Population"
    headers = list(df.index)
    df.insert(loc=0, column=index_name, value=headers)
    sheet = to_sheet(df)
    format_cells(sheet, money)
    sheet.row_headers = False
    return sheet


def display_population(sheet, money=False, round=False):
    """Display sheet with specific, population-optimized formatting."""
    sheet = format_population(sheet, money=money, round=round)
    display(sheet)


def generate_pie_chart(df, title="", show_decimal=False):
    fig = plt.figure(title=title)

    pie_chart = plt.pie(
        sizes=df.values.tolist(),
        labels=df.index.values.tolist(),
        display_labels="outside",
        colors=chart_colors[: df.index.values.size],
        display_values=True,
    )
    if not show_decimal:
        pie_chart.values_format = "0"
    return fig


def generate_bar(df, title="", scientific_notation=False, small_xlabel=False):
    fig = plt.figure(title=title)
    x_vals = df.index.values.tolist()
    if len(x_vals) > 5:
        small_xlabel = True
    x_titles = []
    for val in x_vals:
        if len(val.split(" ")) < 3:
            x_titles.append(val)
        else:
            x_titles.append(" ".join(val.split(" ")[:2]))
    bar_chart = plt.bar(
        x=x_titles, y=df, colors=chart_colors[: df.index.values.size]
    )
    if small_xlabel:
        fig.axes[0].tick_style = {"font-size": "6"}
    if not scientific_notation:
        fig.axes[1].tick_format = ".1f"
    return fig


def generate_group_bar(df, title="", scientific_notation=False):
    fig = plt.figure(title=title)
    bar_chart = plt.bar(
        x=df.columns.values.tolist(),
        y=df,
        labels=df.index.values.tolist(),
        display_legend=False,
        type="grouped",
        colors=chart_colors[: df.index.values.size],
    )
    if df.columns.name:
        plt.xlabel(df.columns.name.rsplit(" ", 1)[0])
    plt.ylim(0, np.amax(df.values))
    if not scientific_notation:
        fig.axes[1].tick_format = ".1f"
    return fig


def generate_scatter(
    df, title="", scientific_notation=False, small_xlabel=True
):
    fig = plt.figure(title=title)
    x_vals = df.index.values.tolist()
    if len(x_vals) > 5:
        small_xlabel = True
    x_titles = []
    for val in x_vals:
        if len(val.split(" ")) < 3:
            x_titles.append(val)
        else:
            x_titles.append(" ".join(val.split(" ")[:2]))
    scatter = plt.scatter(x=x_titles, y=df)

    if small_xlabel:
        fig.axes[0].tick_style = {"font-size": "6"}
    if not scientific_notation:
        fig.axes[1].tick_format = ".1f"
    return fig


def generate_stacked_bar(df, title="", scientific_notation=False):
    fig = plt.figure(title=title)

    bar_chart = plt.bar(
        x=df.columns.values.tolist(),
        y=df,
        labels=df.index.values.tolist(),
        display_legend=False,
        type="stacked",
        colors=chart_colors[: df.index.values.size],
    )
    if df.columns.name:
        plt.xlabel(df.columns.name.rsplit(" ", 1)[0])
    plt.ylim(0, np.amax(df.values))
    if not scientific_notation:
        fig.axes[1].tick_format = ".1f"
    return fig


def generate_separate_bar_list(
    df, scientific_notation=False, small_xlabel=False
):  # returns list, NOT widget
    bar_list = []
    for col in df.columns:  # .values.tolist()
        bar_list.append(
            generate_bar(
                df[col][df[col] != 0],
                title=col,
                scientific_notation=scientific_notation,
                small_xlabel=small_xlabel,
            )
        )
    return bar_list


def generate_separate_scatter_list(
    df, scientific_notation=False, small_xlabel=False
):  # returns list, NOT widget
    scatter_list = []
    for col in df.columns:  # .values.tolist()
        scatter_list.append(
            generate_scatter(
                df[col][df[col] != 0],
                title=col,
                scientific_notation=scientific_notation,
                small_xlabel=small_xlabel,
            )
        )
    return scatter_list


def generate_html_legend(df, colors=chart_colors, table=True, font_size=13):
    name = df.index.name.rsplit(" ", 1)[0]
    html_string = f"<div style='font-size:{font_size}px; font-family:helvetica'><b style='font-weight:bold'>{name}</b>"
    indices = df.index.values
    if table:
        html_string += "<table><tr>"
        for i in range(0, indices.size):
            if i % 2 == 0:
                index_num = int(i / 2)
            else:
                index_num = int(i / 2 + indices.size / 2)
            html_string += f"<td style='padding:0 5px'><span style='color:{colors[index_num]}'>█</span> {indices[index_num]}</td>"
            if i % 2 != 0:
                html_string += "</tr><tr>"
        html_string += "</tr></table>"
    else:
        for_count = 0
        for string in indices:
            if for_count == 0:
                html_string += "<br>"
            else:
                html_string += "&emsp;"
            html_string += (
                f"<span style='color:{colors[for_count]}'>█</span> {string}"
            )
            for_count += 1
    html_string += "</div>"
    return widgets.HTML(html_string)


def generate_group_bar_legend(
    df, title="", scientific_notation=False, legend_table=True
):
    chart = generate_group_bar(
        df, title=title, scientific_notation=scientific_notation
    )
    legend = generate_html_legend(df, table=legend_table)
    return widgets.VBox([chart, legend])


def generate_stacked_bar_legend(
    df, title="", scientific_notation=False, legend_table=True
):
    chart = generate_stacked_bar(
        df, title=title, scientific_notation=scientific_notation
    )
    legend = generate_html_legend(df, table=legend_table)
    return widgets.VBox([chart, legend])


def triangular(a, b, c):
    return math.sqrt(((a * a + b * b + c * c) - a * b - a * c - b * c) / 18)
