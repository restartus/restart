"""Demand Rates from Washington from the v1.x Surge spreadsheet.

The original model based on DOH levels
"""
from typing import List, Optional

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from demand import Demand
from load_csv import LoadCSV
from log import Log
from population import Population
from resourcemodel import Resource
from util import datetime_to_code


class DemandWA(Demand):
    """Calculate demand using default WA estimates.

    Overrides the Demand class
    """

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population,
        res: Resource,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the DataFrames.

        Calculate demand for resources by populations
        TODO: Add organization demand so dimensions become p+o
        """
        super().__init__(config, pop, res, log_root=log_root)

        if config is None:
            raise ValueError(f"{config=} is null")

        # now override the variables you want changed
        try:
            source = config["Paths"].get()
            source = LoadCSV(source=source).data
        except KeyError:
            pass

        if pop.population_pP_tr is None:
            raise ValueError("pop.population_pP_tr")

        # self.level_pl_arr = self.calculate_essential(map_df, config, pop)
        # self.level_pl_df = pd.DataFrame(
        #     self.level_pl_arr,
        #     index=pop.population_pP_tr.index,
        #     columns=pop.population_pP_tr.columns,
        # )
        # log.debug(f"{self.level_pl_df=}")

        # Now calculate everything
        self.recalc(pop, res)

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
        if pop.population_pP_tr is None:
            raise ValueError("pop.population_pP_df")
        # population_pP_df: pd.DataFrame = pop.population_pP_tr.df
        # TODO: I don't know what this is RichC;W
        # pop.codes = None
        # if pop.codes is None or df is None:
        #     arr = np.random.rand(detail_pd_df.shape[0], 2)
        #     return np.rint(arr)
        # manually redo indexing and select the rows we need
        df.columns = df.iloc[2528]
        df = df.iloc[2529:3303]
        df = df[["SOC", "Essential (0 lowest)"]]

        # if pop.codes is None:
        #     return np.array(
        #         config["Data"]["Population p"]["Pop to Level pl"].get()
        #    )

        # add the codes back in
        pop_level: List = []
        df["SOC"] = df["SOC"].apply(datetime_to_code)
        df.reset_index(drop=True, inplace=True)
        # for code in list(pop.codes):
        #     arr = np.zeros(2)
        #     try:
        #         ind = df[df["SOC"] == code].index[0]
        #     except IndexError:
        #          ind = -1
        #     if ind > 0:
        #         level = df.iloc[ind]["Essential (0 lowest)"]
        #     else:
        #         level = np.random.randint(0, high=6)
        #   if level >= 5:
        #       arr[0] = 1
        #   else:
        #       arr[1] = 1
        #   pop_level.append(arr)

        return np.array(pop_level)
