"""Get Demand Rates from Dictionary.

The original model based on DOH levels
"""
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from data import Data
from demand import Demand
from log import Log
from population import Population
from resourcemodel import Resource


class DemandDict(Demand):
    """Calculate demand reading from the data dictionary.

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
        """Initialize Demand of Resources.

        Calculates the total, costs and per capita demand
        """
        super().__init__(config, log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        self.demand_per_unit_map_dn_um = Data(
            "demand_per_unit_map_dn_um", config, log_root=log_root
        )
        log.debug(f"{self.demand_per_unit_map_dn_um.df=}")

        # original matrix multiply to get per person demands
        # self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
        #     self.level_to_res_mn_df
        # )

        self.demand_by_pop_per_person_pn_uc = Data(
            "demand_by_pop_per_person_pn_uc", config, log_root=log_root
        )

        self.demand_by_pop_per_person_pn_uc.array = (
            pop.pop_demand_per_unit_map_pd_um.array
            @ self.demand_per_unit_map_dn_um.array
        )
        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        # Einsum equivalent for automatic generation
        test = np.einsum(
            "pd,dn->pn",
            pop.pop_demand_per_unit_map_pd_um.array,
            self.demand_per_unit_map_dn_um.array,
        )
        log.debug(f"{test=}")
        if np.array_equal(self.demand_by_pop_per_person_pn_uc.array, test):
            log.debug("einsum works!")

        self.demand_by_pop_total_pn_tc = Data(
            "demand_by_pop_total_pn_tc", config, log_root=log_root
        )
        # Note there is a big hack here as we should really calculate
        # demand across many parameters, but we just pick size
        # self.total_demand_pn_arr = (
        #   np.array(self.demand_pn_df).T * np.array(pop.detail_pd_df["Size"])
        # ).T
        # uses a double transpose because broadcast
        # https://numpy.org/doc/stable/user/basics.broadcasting.html
        # broadcast means start from the lowest dimension
        # each dimenion must match from left to right of be one
        # so if we have pn = (2,9) and p = (2,) we need to invert
        # them to be np=(9,2) and p =(1,2) note that 2, must be converted
        # to a real column matrix
        # Also the size only is just a vector so you need newaxis to promote it
        # https://stackoverflow.com/questions/29241056/how-does-numpy-newaxis-work-and-when-to-use-it
        self.demand_by_pop_total_pn_tc.array = (
            self.demand_by_pop_per_person_pn_uc.array.T
            * pop.population_pP_tr.df["Size"].to_numpy().T
        ).T
        log.debug(f"{self.demand_by_pop_total_pn_tc.df=}")
        test = np.einsum(
            "pn,p->pn",
            self.demand_by_pop_per_person_pn_uc.array,
            pop.population_pP_tr.df["Size"].to_numpy(),
        )
        log.debug(f"{test=}")
        if np.array_equal(self.demand_by_pop_per_person_pn_uc.array, test):
            log.debug("einsum works!")

        # TODO: Convert this single level calculation to a general one based on
        # a dictionary of conversion

        # Original math put the level or popsum1 data here now move to
        # population
        # self.level_demand_ln_df = np.array(self.level_pl_df).T @ np.array(
        #     self.demand_pn_df
        # )
        # need to instantiate variables first
        self.demand_by_popsum1_per_person_p1n_uc = Data(
            "demand_by_popsum1_per_person_p1n_uc", config, logroot=log_root
        )
        # then add to them
        self.demand_by_popsum1_per_person_p1n_uc.array = (
            pop.pop_to_popsum1_per_unit_map_pp1_us.array
            @ self.demand_by_pop_per_person_pn_uc.array
        )
        log.debug(f"{self.demand_by_popsum1_per_person_p1n_uc.df=}")
        # Einsum equivalent of the above, we use x since index needs to be a
        # single character
        test = np.einsum(
            "px,pn->xn",
            pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_per_person_pn_uc.array,
        )
        log.debug(f"{test=}")
        if np.array_equal(
            self.demand_by_popsum1_per_person_p1n_uc.array, test
        ):
            log.debug("einsum works!")

        # TODO: Eventually we will want to calculate this iteration
        # across all summaries so p -> p1 -> p2...
        # And do this in a function because demand for instance
        # should not have to know the population dimension
        self.demand_by_popsum1_total_p1n_tc = Data(
            "demand_by_popsum1_total_p1n_tc", config, log_root=log_root
        )
        # Original math
        # self.level_total_demand_ln_df = (
        #    self.level_pl_df.T @ self.total_demand_pn_df
        # )
        self.demand_by_popsum1_total_p1n_tc.array = (
            pop.pop_to_popsum1_per_unit_map_pp1_us.array.T
            @ self.demand_by_pop_total_pn_tc.array
        )
        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        test = np.einsum(
            "px,pn->xn",
            pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_total_pn_tc.array,
        )

        self.demand_by_popsum1_total_cost_p1n_xc = Data(
            "demand_by_popsum1_total_cost_p1n_xc", config, log_root=log_root
        )
        log.debug(f"{self.demand_by_popsum1_total_cost_p1n_xc.df=}")
        # original formula
        # self.level_total_cost_ln_df = (
        #       self.level_total_demand_ln_df * cost_ln_df.values)
        self.demand_by_popsum1_total_cost_p1n_xc.array = (
            self.demand_by_popsum1_total_p1n_tc.array
            * res.res_by_popsum1_cost_per_unit_p1n_us.array
        )
