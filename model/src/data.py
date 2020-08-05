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
from typing import Dict, List, Optional, Tuple

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

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
        array: np.ndarray,
        description: str,
        config: confuse.Configuration,
        index: str,
        columns: str,
        label: Optional[List[Dict]] = None,
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

        self.config = config
        self.index = index
        self.columns = columns

        self.description = description
        self.label = label
        self.array = array

    # these are the functions called when something externally is changed
    @property
    def array(self):
        """Property method for array.

        Returns the private variable
        """
        return self._array

    @array.setter
    def array(self, array: np.ndarray):
        """Change display and graph values when array changes.

        When this changes update other representations
        """
        if self.config is None:
            raise ValueError(f"{self.config=} is null")
        self._array = array
        self.set_df(
            self.config["Label"].get(), index=self.index, columns=self.columns,
        )
        self.set_alt()

    @property
    def df(self):
        """Property method for df.

        Returns the private variable
        """
        return self._df

    @df.setter
    def df(self, df: pd.DataFrame) -> Data:
        """Change the array and narrow when df changes."""
        self._df = df
        self.set_array(self._df)
        self.set_alt()
        return self

    @property
    def alt(self):
        """Property method for narrow."""
        return self._narrow

    @alt.setter
    def alt(self, alt: pd.DataFrame):
        self._alt = alt
        return self

    # set functions called internally after external changes made
    def set_array(self, df: pd.DataFrame):
        """Change the array when df changes."""
        self._array = np.array(df)

    def set_df(
        self,
        label: Optional[Dict],
        index: Optional[str] = None,
        columns: Optional[str] = None,
    ):
        """Change the df when array changes."""
        df = pd.DataFrame(
            self.array,
            index=label[index]
            if label is not None and index is not None
            else None,
            columns=label[columns]
            if label is not None and columns is not None
            else None,
        )

        df.index.name = index
        df.columns.name = columns

        self._df = df

    def set_alt(self):
        """Convert self.wide to self.narrow."""
        narrow = self.df.reset_index()
        narrow = narrow.melt()
        self._narrow = narrow

    def from_narrow_to_wide(self) -> Data:
        """Convert narrow to wide dataframe."""
        self.log.debug("not implemented")
        return self

    def from_wide_to_array(self) -> Data:
        """Convert wide to a multi-dimenstional array."""
        self.log.debug("not implemented")
        self.array = self.df.to_numpy()
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
