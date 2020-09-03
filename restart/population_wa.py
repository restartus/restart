"""Population reading from QCEW data."""
import math
import os
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from filtermodel import Filter
from load_csv import LoadCSV
from log import Log
from population import Population
from util import load_dataframe


class PopulationWA(Population):
    """NAICS codes for Washington."""

    def __init__(
        self,
        config: confuse.Configuration,
        filt: Filter,
        log_root: Optional[Log] = None,
    ):
        """Initialize.

        Read the paths in and create dataframes, generate mappings
        """
        self.root_log: Optional[Log]
        # global log
        # log: logging.Logger = logging.getLogger(__name__)

        super().__init__(config, log_root=log_root)
        log = self.log
        log.debug(f"module {__name__=}")

        # get location and population from the filter
        self.location = filt.location
        try:
            if self.location["county"] is not None:
                self.location["county"] += " County"
        except KeyError:
            log.debug("invalid location input {self.location=}")
            return

        self.subpop = filt.subpop
        self.config = config

        source = config["Paths"].get()
        source = LoadCSV(source=source).data
        map_df = self.format_map(
            load_dataframe(os.path.join(source["Root"], source["MAP"]))
        )
        self.get_population(map_df)
        self.create_map(map_df)

    def get_population(self, map_df: pd.DataFrame):
        """Get the population numbers."""
        # select the rows we want
        if map_df is None:
            raise ValueError(f"{map_df=} is null")
        if self.config is None:
            raise ValueError(f"{self.config=} is null")

        df = map_df[
            ["Industry description", "6-digit NAICS", "Average employment"]
        ]
        # select just the 6-digit codes
        df = df[df["6-digit NAICS"].apply(lambda x: len(str(x)) == 6)]
        self.detail_pd_df = df.drop("6-digit NAICS", axis=1)
        self.detail_pd_df.columns = ["Industry description", "Size"]
        self.detail_pd_df.set_index(
            "Industry description", drop=True, inplace=True
        )
        self.detail_pd_arr = np.array(self.detail_pd_df)
        self.set_description(
            f"{self.detail_pd_df=}",
            self.config["Description"]["Population p"]["Pop Detail pd"].get(),
        )
        self.log.debug(f"{self.description['detail_pd_df']=}")

    def format_map(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manually slice the excel model to get protection level mappings.

        Args:
            df: The excel model loaded into a dataframe

        Returns:
            The dataframe sliced to give the mappings
        """
        # manually redo indexing and select the rows we need
        # TODO: un-hardcode
        cols = df.iloc[672].dropna()
        df.columns = df.iloc[672]
        df = df.iloc[674:1937]
        df = df[cols]
        df = df.replace(to_replace="*", value=1)

        return df

    def create_map(self, map_df: pd.DataFrame):
        """Generate mappings for NAICS codes and population levels.

        Args:
            df: A dataframe that has NAICS codes

        Returns:
            Dictionary of the population level mappings
        """
        df = map_df[
            [
                "Industry description",
                "6-digit NAICS",
                "Average employment",
                "Protection level",
            ]
        ]

        detailed = df[df["6-digit NAICS"].apply(lambda x: len(str(x)) == 6)]
        medium = df[df["6-digit NAICS"].apply(lambda x: len(str(x)) == 3)]
        major = df[
            df["6-digit NAICS"].apply(
                lambda x: len(str(x)) == 2 or "-" in str(x)
            )
        ]

        map_arr = []

        # TODO: AAAAAHHHHHH THIS IS SO UGLY
        for code in detailed["6-digit NAICS"]:
            arr = np.zeros(7)
            try:
                series = major[
                    major["6-digit NAICS"]
                    .astype(str)
                    .str.contains(str(code)[:2])
                ]["Protection level"]
                if pd.isnull(series.to_numpy()).any():
                    series = medium[
                        medium["6-digit NAICS"]
                        .astype(str)
                        .str.contains(str(code)[:3])
                    ]["Protection level"]
                    if pd.isnull(series.to_numpy()).any():
                        raise IndexError("Subtract 1 and search again")
                level = list(series)[0]
            except IndexError:
                try:
                    code = int(str(code)[:2]) - 1
                    series = major[
                        major["6-digit NAICS"]
                        .astype(str)
                        .str.contains(str(code))
                    ]["Protection level"]
                    if pd.isnull(series.to_numpy()).any():
                        raise IndexError("Everything failed")
                    level = list(series)[0]
                except IndexError:
                    level = 4.0

            if level % 1 == 0:
                arr[int(level)] = 1
            else:
                arr[math.floor(level)] = 0.5
                arr[math.ceil(level)] = 0.5

            map_arr.append(arr)

        if self.config is None:
            raise ValueError("{self.config=} is null")

        self.level_pm_arr = np.array(map_arr)
        self.level_pm_df = pd.DataFrame(
            self.level_pm_arr,
            index=detailed["Industry description"],
            columns=self.config["Label"]["Demand m"].get(),
        )
        self.level_pm_labs = list(self.level_pm_df.index)
        self.set_description(
            f"{self.level_pm_df=}",
            self.config["Description"]["Population p"]["Protection pm"].get(),
        )
        self.log.debug(f"{self.description['level_pm_df']=}")
