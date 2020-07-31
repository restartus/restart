"""Get Demand Rates from Dictionary.

The original model based on DOH levels
"""
import logging
from typing import Dict, Optional

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from demand import Demand
from modeldata import ModelData
from population import Population
from resourcemodel import Resource
from util import Log, set_dataframe


class DemandDict(Demand):
    """Calculate demand reading from the data dictionary.

    Overrides the Demand class
    """

    def __init__(
        self,
        data: ModelData,
        label: Dict,
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
        super().__init__(data, log_root=log_root)
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"In {__name__}")

        self.level_to_res_mn_arr = np.array(
            data.value["Demand m"]["Level to Resource mn"]
        )
        self.level_to_res_mn_df = set_dataframe(
            self.level_to_res_mn_arr,
            label=data.label,
            index=index,
            columns=columns,
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

        self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
            self.res_demand_mn_df
        )
        self.demand_pn_df = pd.DataFrame(
            self.demand_pn_arr,
            index=label["Population p"],
            columns=label["Resource n"],
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

        self.level_pl_arr = data.value["Population p"]["Pop Level l"]
        self.level_pl_df = pd.DataFrame(
            self.level_pl_arr,
            index=data.label["Population p"],
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
            index=label["Population p"],
            columns=label["Resource n"],
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
