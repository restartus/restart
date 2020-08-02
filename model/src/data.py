"""Base class for our own Data.

Since we are doing multity dimensional math, we need to keep three data
structures in sync:

    - The Numpy array that is multiple dimensions
    - A "wide" DataFrame using Multiindex that compresses these to 2-D to be
      used for printing and tabular displa
    - A "narrow" with reset_index and melt that has a single column of data
    and all the rest is encoded in a huge label set
    - It also carries a description, labels and other meta data

The idea is that when the numpy array changes, then we automatically update the
other two representations

TODO: Not implemented need to work out multiindex

"""
from __future__ import annotations

import logging
from typing import Dict, List, Tuple

import numpy as np  # type:ignore
import pandas as pd  # type:ignore

from util import Log


class Data:
    """Base data class for the entire model.

    The main data is in an Numpy array
    The meta data is
        - description. Markdown text describing the data
        - labels. An ordered list that is the axis name and the columns
           for each
                  As an example a 3-D numpy array would have
                  [ Type: "Resource n"
                    Kind: ["N95", "ASTM-3 Mask"]],
                  [ Type: "Attribute a"
                    Kind: ["Unit", "Volume", "Area"]]

    The output data is
        - df(). Suitable for display
        - narrow(). Suitable for graphing
    """

    # do not put variable here unless you want them the same
    # across all classes see https://docs.python.org/3/tutorial/classes.html

    # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    def __init__(
        self,
        array: np.array,
        description: str,
        label: List[Dict],
        log_root: Log = None,
    ):
        """Set base varabiles.

        Mainly the descriptions
        """
        # since we have no log otherwise
        self.log_root = log_root
        if log_root is not None:
            log: logging.Logger = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"{__name__=}")

        self.description = description
        self.label = label
        self.set_array(array)

    def set_array(self, array: np.ndarray) -> Data:
        """Change display and graph values when array changes.

        When this changes update other representations
        """
        self.array = array
        self.df = pd.DataFrame(self.array)
        self.to_narrow()

        return self

    def set_df(self, df: pd.DataFrame) -> Data:
        """Change the array and narrow when df changes."""
        self.df = df
        self.array = df.to_numpy()
        return self

    def set_narrow(self, narrow: pd.DataFrame) -> Data:
        """Given a new narrow, update wide and array."""
        self.narrow = narrow
        self.from_narrow_to_wide()
        self.from_wide_to_array()
        self.log.debug("not implemented")
        return self

    def from_narrow_to_wide(self) -> Data:
        """Convert narrow to wide dataframe."""
        self.log.debug("not implemented")
        return self

    def from_wide_to_array(self) -> Data:
        """Convert wide to a multi-dimenstional array."""
        self.log.debug("not implemented")
        self.array = self.df.to_numpy()
        return self

    def to_narrow(self) -> Data:
        """Convert self.wide to self.narrow."""
        self.narrow = self.df.reset_index()
        self.narrow = self.narrow.melt()
        return self

    def __iter__(self):
        """Iterate over all Pandas DataFrames.

        Uses a list of all frames
        """
        self.df_list = [
            k for k, v in vars(self).items() if isinstance(v, pd.DataFrame)
        ]
        self.df_len = len(self.df_list)
        self.df_index = 0
        return self

    def __next__(self) -> Tuple[str, pd.DataFrame]:
        """Next Pandas DataFrame.

        Iterates through the list of dataframes
        """
        if self.df_index >= self.df_len:
            raise StopIteration
        key = self.df_list[self.df_index]
        value = vars(self)[key]
        self.df_index += 1
        return key, value
