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
"""
from __future__ import annotations

from typing import Tuple

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from base import BaseLog
from log import Log


class Data(BaseLog):
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

    You can override what is in config by passing keyword arguments
    like
        Data(label="Overriding Label"
    The output data is
        - .array numpy array for computation
        - .df Suitable for display
        - .narrow Suitable for graphing

    Uses config for initial configuration but probably that should be a
    subclass of this as config can come in differently


    """

    # do not put variable here unless you want them the same
    # across all classes see https://docs.python.org/3/tutorial/classes.html

    # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    def __init__(
        self,
        key,
        config: confuse.Configuration,
        log_root: Log = None,
        **kwargs,
    ):
        """Set base variables.

        Mainly the descriptions
        """
        # Sets logging
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"{__name__=}")

        self.key: str = key
        self.config_cf: confuse.Configuration = config

        # Override the YAML with a dictionary
        # https://confuse.readthedocs.io/en/latest/
        # https://www.pythoncentral.io/how-to-check-if-a-list-tuple-or-dictionary-is-empty-in-python/
        if kwargs:
            for k, v in kwargs.items():
                if "index" in k:
                    k = k.split("_")[0]
                    ind = [
                        i
                        for i in config["Model"][self.key]["index"].get()
                        if f"({k})" in i
                    ][0]
                    args = {"Dimension": {ind: v}}
                else:
                    args = {"Model": {self.key: {k: v}}}

                config.set_args(args, dots=True)

        self.data_cf: confuse.Configuration = config["Model"][key]
        self.dimension_cf: confuse.Configuration = config["Dimension"]
        self.index_cf: confuse.Configuration = self.data_cf["index"]

        self._array: np.ndArray = None
        self._df: pd.DataFrame = None
        self._narrow: pd.DataFrame = None

        # if there is no value it is a calculate amount and fill with NaNs
        try:
            self._array = np.array(self.data_cf["array"].get())
        # user create exceptions must include the import module name
        # https://www.geeksforgeeks.org/user-defined-exceptions-python-examples/
        except confuse.NotFoundError:
            log.debug(f"set null array based on {self.index_cf.get()=}")
            shape = [
                len(self.dimension_cf[x].get()) for x in self.index_cf.get()
            ]
            log.debug(f"of {shape=}")
            self._array = np.empty(
                [len(self.dimension_cf[x].get()) for x in self.index_cf.get()]
            )

        log.debug(f"{self._array=}")

        self.set_df()

    # https://www.journaldev.com/22460/python-str-repr-functions
    # so debugging make sense this does not work because
    # if called early _df and others are not available
    # def __repr__(self):
    #     """Show more than just the type."""
    # return {"df": self._df, "array": self._array, "narrow": self._narrow}

    # Three data structures that
    # can change and then the other two must switch:
    # TODO: Instead of all this manually, change so that we have a
    # an array of transforms so we can index in and call a function
    # The call will look like transform = [ unity, to_numpy ], [ to_df, unity
    # ]]
    # and then the generic function is convert[from][to]
    # - array. This is the numpy array
    # - df. This is the wide format dataframe suitable for printing
    # - narrow. This is the narrow frame for charting
    # Each setter when called must active the other two
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

        When this changes update other representations such as the df and wide
        """
        if self.config_cf is None:
            raise ValueError(f"{self.config_cf=} is null")
        self._array = array
        self.set_df()
        # note set_narrow assumes set_df is done first
        self.set_narrow()

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
        self.set_narrow()
        return self

    @property
    def narrow(self):
        """Property method for narrow form used for charting."""
        return self._narrow

    # TODO: Not implemented should rebuild the indices
    @narrow.setter
    def narrow(self, narrow: pd.DataFrame):
        self._narrow = narrow
        return self

    # set functions called internally after external changes made
    def set_array(self, df: pd.DataFrame):
        """Change the array when df changes."""
        self._array = np.array(df)

    def set_df(self):
        """Change the df when array changes in self._array.

        The normal 2D case when len(dimensions) <=2
        dimension[0] or index is the list of row names
            (e.g., ["Healthcare", "Non-healthcare"])
        dimension[1] or columns is the list of column names
            (e.g., ["N95", "Surgical Mask"])
        index[0] or index_name is name of index  (e.g., "Population")
        index[1] column_name is the name of all the columns (e.g., "Resource")

        The 3D cases we use a multiindex when len(dimensions) >2
        index is a list of a list of row names  for the 1..N-1 dimensions
            [["Min Inv", "EOQ Inv", "Order Size"], ["HC", "Non-HC"]]
        dimension[-1] or columns is the value of the last dimension
        index[-1] or column_name is the same just for the Nth index
        dimension[:-1] or the 1st to N-1st dimensions
        index[:-1] index_name is a list ["Inv", "Population"]

        Note that if you change the data value, the only way to do it appears
        to be to construct a new DataFrame
        https://note.nkmk.me/en/python-pandas-numpy-conversion/
        """
        # Assume that once we set the Data we never change the
        # dimensions or lables, but only the data inside
        self.index_name = self.index_cf.get()[:-1]
        self.columns_name = self.index_cf.get()[-1]
        self.columns = self.dimension_cf[self.columns_name].get()
        if len(self.index_name) <= 1:
            # this is two dimensional
            # https://stackoverflow.com/questions/18691084/what-does-1-mean-in-numpy-reshape
            # Also note that we need .get for a confus object
            # And need to dereference the index_name
            self.index_name = self.index_name[0]
            self.index = self.dimension_cf[self.index_name].get()
            df = pd.DataFrame(
                self.array,
                index=self.index,
                columns=self.columns,
            )
            df.index.name = self.index_name
        else:
            # flatten the array into 2D so only column is there
            # first -1 means compute it, second -1 means last dimension
            self.flat2d_arr = self.array.reshape(-1, self.array.shape[-1])
            # Do a lookup of the index in dimension
            # https://stackoverflow.com/questions/49542348/using-a-list-comprehension-to-look-up-variables-works-with-globals-but-not-loc/49542378
            self.index = [self.dimension_cf[x].get() for x in self.index_name]
            self.multi_index = pd.MultiIndex.from_product(
                self.index,
                names=self.index_name,
            )
            # https://docs.heliopy.org/en/0.1b5/examples/multiindex.html
            df = pd.DataFrame(
                self.flat2d_arr,
                index=self.multi_index,
                columns=self.columns,
            )
        df.columns.name = self.columns_name
        self._df = df

    def set_narrow(self):
        """Convert self.wide to self.narrow."""
        narrow = self.df.reset_index()
        narrow = narrow.melt()
        self._narrow = narrow

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
