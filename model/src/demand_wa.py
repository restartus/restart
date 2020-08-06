"""Demand Rates from Washington from the v1.x Surge spreadsheet.

The original model based on DOH levels
"""
import logging
import os
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from demand import Demand
from load_csv import LoadCSV
from population import Population
from resourcemodel import Resource
from util import Log, datetime_to_code, load_dataframe, set_dataframe


class DemandWA(Demand):
    """Calculate demand using default WA estimates.

    Overrides the Demand class
    """

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the dataframes.

        Do some matrix math
        """
        super().__init__(config, log_root=log_root)
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"In {__name__}")

        map_df: Optional[pd.DataFrame] = None

        try:
            source = config["Paths"].get()
            source = LoadCSV(source=source).data
            map_df = load_dataframe(
                os.path.join(source["Root"], source["MAP"])
            )
        except KeyError:
            pass

        self.level_to_res_mn_arr = config["Data"]["Demand m"][
            "Level to Resource mn"
        ].get()
        self.level_to_res_mn_df = set_dataframe(
            self.level_to_res_mn_arr,
            label=config["Label"].get(),
            index="Demand m",
            columns="Resource n",
        )
        log.debug(f"{self.level_to_res_mn_df=}")
        self.set_description(
            f"{self.level_to_res_mn_df=}",
            config["Description"]["Demand m"]["Demand Resource mn"].get(),
        )

        # protection level rates
        if pop is None:
            raise ValueError("{pop=} should not be None")
        if res is None:
            raise ValueError("{res=} should not be None")

        self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
            self.level_to_res_mn_df
        )
        self.demand_pn_df = pd.DataFrame(
            self.demand_pn_arr,
            index=pop.level_pm_labs,
            columns=config["Label"]["Resource n"].get(),
        )

        log.debug(f"{self.demand_pn_df=}")
        self.demand_pn_df.index.name = "Population p"
        self.demand_pn_df.columns.name = "Resource n"
        self.set_description(
            f"{self.demand_pn_df=}",
            config["Description"]["Population p"][
                "Population Demand pn"
            ].get(),
        )

        if pop.detail_pd_df is None:
            raise ValueError(f"{pop.detail_pd_df=} should not be None")

        if pop.detail_pd_arr is None:
            raise ValueError(f"{pop.detail_pd_df=} should not be None")

        self.level_pl_arr = self.calculate_essential(map_df, config, pop)
        self.level_pl_df = pd.DataFrame(
            self.level_pl_arr,
            index=pop.level_pm_labs,
            columns=config["Label"]["Pop Level l"].get(),
        )
        log.debug(f"{self.level_pl_df=}")
        self.set_description(
            f"{self.level_pl_df=}",
            config["Description"]["Population p"]["Pop to Level pl"].get(),
        )

        self.level_demand_ln_df = np.array(self.level_pl_df).T @ np.array(
            self.demand_pn_df
        )

        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
            f"{self.level_demand_ln_df=}",
            config["Description"]["Population p"]["Level Demand ln"].get(),
        )

        self.total_demand_pn_arr = (
            np.array(self.demand_pn_df).T * np.array(pop.detail_pd_df["Size"])
        ).T
        self.total_demand_pn_df = pd.DataFrame(
            self.total_demand_pn_arr,
            index=pop.level_pm_labs,
            columns=config["Label"]["Resource n"].get(),
        )

        self.total_demand_pn_df.index.name = "Population p"
        log.debug(f"{self.total_demand_pn_df=}")
        self.set_description(
            f"{self.total_demand_pn_df=}",
            config["Description"]["Population p"][
                "Population Total Demand pn"
            ].get(),
        )

        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        log.debug(f"{self.level_total_demand_ln_df=}")
        self.set_description(
            f"{self.level_total_demand_ln_df=}",
            config["Description"]["Population p"][
                "Level Total Demand ln"
            ].get(),
        )

        self.level_total_cost_ln_df = None
        self.set_description(
            f"{self.level_total_cost_ln_df=}",
            config["Description"]["Population p"]["Level Total Cost ln"].get(),
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
        self, df: pd.DataFrame, config: confuse.Configuration, pop: Population
    ) -> pd.DataFrame:
        """Get population essential levels from the excel model.

        Manually slice the dataframe
        """
        if pop.codes is None or df is None:
            return np.array(
                config["Data"]["Population p"]["Pop to Level pl"].get()
            )

        # manually redo indexing and select the rows we need
        df.columns = df.iloc[2528]
        df = df.iloc[2529:3303]
        df = df[["SOC", "Essential (0 lowest)"]]

        if pop.codes is None:
            return np.array(
                config["Data"]["Population p"]["Pop to Level pl"].get()
            )

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
