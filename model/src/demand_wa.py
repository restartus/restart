"""Demand Rates from Washington from the v1.x Surge spreadsheet.

The original model based on DOH levels
"""
import logging
import os
from typing import Optional, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from demand import Demand
from load_csv import LoadCSV
from modeldata import ModelData
from population import Population
from resourcemodel import Resource
from util import Log, datetime_to_code, load_dataframe


class DemandWA(Demand):
    """Calculate demand using default WA estimates.

    Overrides the Demand class
    """

    def __init__(
        self,
        data: ModelData,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the dataframes.

        Do some matrix math
        """
        super().__init__(data, log_root=log_root)
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"In {__name__}")

        map_df: Optional[pd.DataFrame] = None

        try:
            source = data.datapaths["Paths"]
            source = LoadCSV(source=source).data
            map_df = load_dataframe(
                os.path.join(source["Root"], source["MAP"])
            )
        except KeyError:
            pass

        # read in the burn rates
        (
            self.res_demand_mn_rows,
            self.res_demand_mn_cols,
            self.res_demand_mn_arr,
        ) = self.calculate_burn(map_df, data)

        self.res_demand_mn_df = pd.DataFrame(
            self.res_demand_mn_arr,
            index=self.res_demand_mn_rows,
            columns=self.res_demand_mn_cols,
        )
        log.debug(f"{self.res_demand_mn_df=}")
        self.set_description(
            f"{self.res_demand_mn_df=}",
            data.description["Demand m"]["Demand Resource mn"],
        )

        # protection level rates
        if pop is None:
            raise ValueError("{pop=} should not be None")
        if res is None:
            raise ValueError("{res=} should not be None")

        # TODO: move pop.level_pm_df to demand
        self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
            self.res_demand_mn_df
        )
        self.demand_pn_df = pd.DataFrame(
            self.demand_pn_arr,
            index=pop.level_pm_labs,
            columns=self.res_demand_mn_cols,
        )
        log.debug(f"{self.demand_pn_df=}")
        self.demand_pn_df.index.name = "Population p"
        self.demand_pn_df.columns.name = "Resource n"
        self.set_description(
            f"{self.demand_pn_df=}",
            data.description["Population p"]["Population Demand pn"],
        )

        if pop.detail_pd_df is None:
            raise ValueError(f"{pop.detail_pd_df=} should not be None")

        if pop.detail_pd_arr is None:
            raise ValueError(f"{pop.detail_pd_df=} should not be None")

        self.level_pl_arr = self.calculate_essential(map_df, data, pop)
        self.level_pl_df = pd.DataFrame(
            self.level_pl_arr,
            index=pop.level_pm_labs,
            columns=data.label["Pop Level l"],
        )
        log.debug(f"{self.level_pl_df=}")

        self.level_demand_ln_df = np.array(self.level_pl_df).T @ np.array(
            self.demand_pn_df
        )

        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
            f"{self.level_demand_ln_df=}",
            data.description["Population p"]["Level Demand ln"],
        )

        self.total_demand_pn_arr = (
            np.array(self.demand_pn_df).T * np.array(pop.detail_pd_df["Size"])
        ).T
        self.total_demand_pn_df = pd.DataFrame(
            self.total_demand_pn_arr,
            index=pop.level_pm_labs,
            columns=self.res_demand_mn_cols,
        )

        self.total_demand_pn_df.index.name = "Population p"
        log.debug(f"{self.total_demand_pn_df=}")
        self.set_description(
            f"{self.total_demand_pn_df=}",
            data.description["Population p"]["Population Total Demand pn"],
        )

        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        log.debug(f"{self.level_total_demand_ln_df=}")
        self.set_description(
            f"{self.level_total_demand_ln_df=}",
            data.description["Population p"]["Level Total Demand ln"],
        )

        self.level_total_cost_ln_df = None
        self.set_description(
            f"{self.level_total_cost_ln_df=}",
            data.description["Population p"]["Level Total Cost ln"],
        )

    def level_total_cost(self, cost_ln_df):
        """Calculate the total cost of resource for a population level.

        The total cost of resources
        """
        log = self.log
        self.level_total_cost_ln_df = (
            self.level_total_demand_ln_df * cost_ln_df.values
        )
        log.debug("level_total_cost_ln_df\n%s", self.level_total_cost_ln_df)

        return self

    def calculate_essential(
        self, df: pd.DataFrame, data: ModelData, pop: Population
    ) -> pd.DataFrame:
        """Get population essential levels from the excel model.

        Manually slice the dataframe
        """
        if pop.codes is None or df is None:
            return np.array(data.value["Population p"]["Pop to Level pl"])

        # manually redo indexing and select the rows we need
        df.columns = df.iloc[2528]
        df = df.iloc[2529:3303]
        df = df[["SOC", "Essential (0 lowest)"]]

        if pop.codes is None:
            return np.array(data.value["Population p"]["Pop to Level pl"])

        # add the codes back in
        pop_level = []
        df["SOC"] = df["SOC"].apply(datetime_to_code)
        df.reset_index(drop=True, inplace=True)
        for code in list(pop.codes):
            arr = np.zeros(2)
            try:
                ind = df[df["SOC"] == code].index[0]
            except IndexError:
                ind = -1

            if ind > 0:
                level = df.iloc[ind]["Essential (0 lowest)"]
            else:
                level = np.random.randint(0, high=6)

            if level >= 5:
                arr[0] = 1
            else:
                arr[1] = 1

            pop_level.append(arr)

        return np.array(pop_level)

    def calculate_burn(
        self, df: pd.DataFrame, data: ModelData,
    ) -> Tuple[list, list, np.ndarray]:
        """Pull for the covid-surge-who model for burn rates.

        Does some dataframe slicing manually
        """
        res_list = data.label["Resource n"]
        df.columns = df.iloc[5]
        df = df.iloc[6:13]
        df = df[res_list].fillna(0)
        arr_rows = list(df["Level"])
        df.drop(["Level"], axis=1, inplace=True)
        arr = np.array(df)
        arr_cols = list(df.columns)
        return arr_rows, arr_cols, arr
