"""Get Demand Rates from Dictionary.

The original model based on DOH levels
"""
import logging
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from demand import Demand
from population import Population
from resourcemodel import Resource
from util import Log, set_dataframe


class DemandDict(Demand):
    """Calculate demand reading from the data dictionary.

    Overrides the Demand class
    """

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population = None,
        res: Resource = None,
        index: Optional[str] = None,
        columns: Optional[str] = None,
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

        self.level_to_res_mn_arr = np.array(
            config["Data"]["Demand m"]["Level to Resource mn"].get()
        )
        self.level_to_res_mn_df = set_dataframe(
            self.level_to_res_mn_arr,
            label=config["Label"].get(),
            index=index,
            columns=columns,
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
        self.demand_pn_df = set_dataframe(
            self.demand_pn_arr,
            label=config["Label"].get(),
            index="Population p",
            columns="Resource n",
        )
        log.debug(f"{self.demand_pn_df=}")
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

        # self.level_pl_arr = data.value["Population p"]["Pop to Level pl"]
        self.level_pl_arr = config["Data"]["Population p"][
            "Pop to Level pl"
        ].get()
        self.level_pl_df = set_dataframe(
            self.level_pl_arr,
            label=config["Label"].get(),
            index="Population p",
            columns="Pop Level l",
        )
        log.debug(f"{self.level_pl_df=}")
        self.set_description(
            f"{self.level_pl_df=}",
            config["Data"]["Population p"]["Pop to Level pl"].get(),
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
        self.total_demand_pn_df = set_dataframe(
            self.total_demand_pn_arr,
            label=config["Label"].get(),
            index="Population p",
            columns="Resource n",
        )
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
