"""Epi Data Read.

Read in the epi from the model dictionary
"""
import os
from typing import Dict, Optional

import confuse  # type: ignore
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore

from util import load_dataframe
from data import Data
from load_csv import LoadCSV
from epi import Epi
from log import Log


class EpiTable(Epi):
    """Epi Data Readers.

    Reads the epi data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Optional[Log] = None,
        type: str = None,
    ):
        """Initialize the epi object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        arr: np.ndarray = self.load_data(config)

        # get epi data
        # Using the new Lucas data class
        self.epi_eE_pr = Data(
            "epi_eE_pr",
            config,
            log_root=self.log_root,
            e_index=["COVID-19"],
            E_index=["Hospitalizations", "Deaths"],
            array=arr,
        )

        log.debug(f"{self.epi_eE_pr.df=}")

    def load_data(self, config):
        """Loads data from Reich Dataframe for specified model type."""
        # extract reich dataframe of selected agg
        source: Dict[str, str] = config["Reich"].get()
        source = LoadCSV(source=source).data

        # agg is just state for now; will take input location
        # from filter object once implemented
        agg: str = "state"
        # WA state fips is 53
        state: int = 53
        model: str = "IHME-CurveFit"

        df: pd.DataFrame = load_dataframe(
            os.path.join(source["Root"], source[agg])
        )

        df = (
            df[(df["location"] == state) & (df["source"] == model)]
            .set_index(["value_unit_target"], drop=True)
            .sort_index()
        )

        # cases = max(df.loc['cases'])
        hosps: int = max(df.loc["hosps"]["value"])
        deaths: int = max(df.loc["deaths"]["value"])

        return np.array([[hosps, deaths]])
