"""Consumption Rates from Washington.

The original model based on DOH levels
"""
import os
import logging
from typing import Optional, Tuple

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from consumption import Consumption
from modeldata import ModelData
from population import Population
from resourcemodel import Resource
from util import Log, load_dataframe
from loader.load_csv import LoadCSV

# TODO: move into resource module
RES_LIST = ['Level', 'N95 + Mask', 'N95', 'ASTM 3 Mask',
            'ASTM 1-2 Mask', 'Non ASTM Mask', 'Face Shield', 'Gowns',
            'Gloves', 'Shoe Covers']


class ConsumptionWA(Consumption):
    """Calculate consumption using default WA estimates.

    Overrides the Consumption class
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

        source = data.datapaths['Paths']
        source = LoadCSV(source=source).data
        map_df = load_dataframe(os.path.join(source['Root'],
                                             source['MAP']))
        (self.res_demand_mn_rows,
         self.res_demand_mn_cols,
         self.res_demand_mn_arr) = self.calculate_burn(map_df)
        self.res_demand_mn_df = pd.DataFrame(
                self.res_demand_mn_arr,
                index=self.res_demand_mn_rows,
                columns=self.res_demand_mn_cols)
        log.debug(f"{self.res_demand_mn_df=}")
        self.set_description(
            f"{self.res_demand_mn_df=}",
            data.description["Consumption m"]["Cons Resource mn"],
        )

        # protection level rates
        if pop is None:
            raise ValueError("{pop=} should not be None")
        if res is None:
            raise ValueError("{res=} should not be None")

        # TODO: move pop.level_pm_df to consumption
        self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
                self.res_demand_mn_df)
        self.demand_pn_df = pd.DataFrame(
                self.demand_pn_arr,
                index=pop.level_pm_labs,
                columns=self.res_demand_mn_cols)
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

        self.level_pl_arr = np.hstack(
            (
                np.ones((pop.detail_pd_df.shape[0], 1)),
                np.zeros((pop.detail_pd_df.shape[0], 1)),
            )
        )

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
                np.array(self.demand_pn_df).T * np.array(
                    pop.detail_pd_df['Size'])).T
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

    def calculate_burn(self,
                       df) -> Tuple[list, list, np.ndarray]:
        """Pull for the covid-surge-who model for burn rates.

        Does some dataframe slicing manually
        """
        df.columns = df.iloc[5]
        df = df.iloc[6:13]
        df = df[RES_LIST].fillna(0)
        arr_rows = list(df['Level'])
        df.drop(['Level'], axis=1, inplace=True)
        arr = np.array(df)
        arr_cols = list(df.columns)
        return arr_rows, arr_cols, arr
