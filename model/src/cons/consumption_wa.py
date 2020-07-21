"""Consumption Rates from Washington.

The original model based on DOH levels
"""
import logging
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from typing import Optional
from modeldata import ModelData
from util import Log, set_dataframe
from consumption import Consumption
from population import Population
from resourcemodel import Resource


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
            type: Optional[str] = None):
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

        # setting burn rate values
        self.res_demand_mn_arr = data.value["Consumption m"][
                                            "Cons Resource mn"]
        self.res_demand_mn_df = set_dataframe(
                self.res_demand_mn_arr,
                data.label,
                index="Consumption m",
                columns="Resource n")
        log.debug(f"{self.res_demand_mn_df=}")
        self.set_description(
                f"{self.res_demand_mn_df=}",
                data.description["Consumption m"]["Cons Resource mn"])

        # protection level rates
        if pop is None:
            raise ValueError("{pop=} should not be None")
        if res is None:
            raise ValueError("{res=} should not be None")

        self.demand_pn_df = pop.level_pm_df @ self.res_demand_mn_df
        log.debug(f"{self.demand_pn_df=}")
        self.demand_pn_df.index.name = "Population p"
        self.demand_pn_df.columns.name = "Resource n"
        self.set_description(
                f"{self.demand_pn_df=}",
                data.description["Population p"]["Population Demand pn"])

        if pop.attr_pd_df is None:
            raise ValueError(f"{pop.attr_pd_df=} should not be None")

        if pop.attr_pd_arr is None:
            raise ValueError(f"{pop.attr_pd_df=} should not be None")

        self.level_pl_arr = np.hstack(
                (np.ones((pop.attr_pd_df.shape[0], 1)),
                 np.zeros((pop.attr_pd_df.shape[0], 1))))

        self.level_pl_df = pd.DataFrame(
                self.level_pl_arr,
                index=pop.level_pm_labs,
                columns=data.label["Pop Level l"])
        log.debug(f"{self.level_pl_df=}")

        self.level_demand_ln_df = np.array(
                self.level_pl_df).T @ np.array(self.demand_pn_df)

        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
                f"{self.level_demand_ln_df=}",
                data.description["Population p"]["Level Demand ln"])

        n95 = np.array(
                self.demand_pn_df['N95 Surgical'] * pop.attr_pd_arr).reshape(
                        [pop.attr_pd_arr.shape[0], 1])
        astm = np.array(
                self.demand_pn_df['ASTM Mask'] * pop.attr_pd_arr).reshape(
                        [pop.attr_pd_arr.shape[0], 1])
        self.total_demand_pn_arr = np.hstack((n95, astm))
        self.total_demand_pn_df = pd.DataFrame(
                self.total_demand_pn_arr,
                index=pop.level_pm_labs,
                columns=data.label["Resource n"])

        self.total_demand_pn_df.index.name = "Population p"
        log.debug(f"{self.total_demand_pn_df=}")
        self.set_description(
                f"{self.total_demand_pn_df=}",
                data.description["Population p"]["Population Total Demand pn"])

        self.level_total_demand_ln_df = (
                self.level_pl_df.T @ self.total_demand_pn_df)
        log.debug(f"{self.level_total_demand_ln_df=}")
        self.set_description(
                f"{self.level_total_demand_ln_df=}",
                data.description["Population p"]["Level Total Demand ln"])
        self.set_description(
                f"{self.level_total_demand_ln_df=}",
                data.description["Population p"]["Level Total Demand ln"])

        self.level_total_cost_ln_df = None
        self.set_description(
                f"{self.level_total_cost_ln_df=}",
                data.description["Population p"]["Level Total Cost ln"])

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
