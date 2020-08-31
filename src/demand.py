"""Demand Model.

Demand modeling
"""
from typing import Dict, Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from base import Base
from data import Data
from log import Log
from population import Population
from resourcemodel import Resource


class Demand(Base):
    """Calculate consumption based on Population and Resource.

    Take in Pop and and Res and into model.data["Pop Res Demand pn"]
    Some parameters are to use:
    - Washington estimate
    - Mitre burn rates
    - Johns Hopkins burn rates
    - CDPH estimates
    - Ensemble

    If pop and res aren't set by default take the existing Population and
    resource already in the model.data

    With dimensions ["Population p"]["Resource n"]

    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        config: confuse.Configuration,
        res: Resource,
        pop: Optional[Population] = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        self.set_data(config, log_root)
        self.pop = pop
        self.res = res

        if pop is not None:
            self.recalc()

    def adjust_burn(self, new_burn):
        """Adjust the burn rates."""
        self.demand_per_unit_map_dn_um.array = new_burn
        self.recalc()

    def set_data(self, config, log_root):
        """Instantiate the base data objects for inheritance purposes."""
        log = self.log

        self.demand_per_unit_map_dn_um = Data(
            "demand_per_unit_map_dn_um", config, log_root=log_root
        )
        log.debug(f"{self.demand_per_unit_map_dn_um.df=}")

        self.demand_by_pop_per_person_pn_uc = Data(
            "demand_by_pop_per_person_pn_uc", config, log_root=log_root
        )

        # need to instantiate variables first

        self.demand_by_pop_total_pn_tc = Data(
            "demand_by_pop_total_pn_tc", config, log_root=log_root
        )

        # not used
        self.demand_by_popsum_ps_us: Optional[Dict] = None

        self.demand_by_popsum1_per_person_p1n_uc = Data(
            "demand_by_popsum1_per_person_p1n_uc", config, log_root=log_root
        )

        self.demand_by_popsum1_total_p1n_tc = Data(
            "demand_by_popsum1_total_p1n_tc", config, log_root=log_root
        )
        # get a range enabled version of the above for inventory
        self.demand_by_popsum1_total_rp1n_tc = Data(
            "demand_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )

        self.demand_by_popsum1_total_cost_p1n_xc = Data(
            "demand_by_popsum1_total_cost_p1n_xc", config, log_root=log_root
        )
        log.debug(f"{self.demand_by_popsum1_total_cost_p1n_xc.df=}")

    def recalc(self):
        """Recalculate all demands.

        Right now it must be run in this order
        """
        self.set_demand_by_pop_per_person_pn_uc()
        self.set_demand_by_pop_total_pn_tc()
        self.set_demand_by_popsum1_per_person_p1n_uc()
        self.set_demand_by_popsum1_total_p1n_tc()
        self.set_demand_by_popsum1_total_cost_p1n_xc()

    def set_demand_by_pop_per_person_pn_uc(self):
        """Sets the Demand by Population Per Person."""
        log = self.log

        # original matrix multiply to get per person demands
        # self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
        #     self.level_to_res_mn_df
        # )

        if self.pop.pop_demand_per_unit_map_pd_um is None:
            raise ValueError("pop.pop_demand_per_unit_map_pd_um")

        self.demand_by_pop_per_person_pn_uc.array = (
            self.pop.pop_demand_per_unit_map_pd_um.array
            @ self.demand_per_unit_map_dn_um.array
        )
        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        # Einsum equivalent for automatic generation
        test = np.einsum(
            "pd,dn->pn",
            self.pop.pop_demand_per_unit_map_pd_um.array,
            self.demand_per_unit_map_dn_um.array,
        )
        log.debug(f"{test=}")
        if not np.array_equal(self.demand_by_pop_per_person_pn_uc.array, test):
            log.critical("einsum fails!")

    def set_demand_by_pop_total_pn_tc(self):
        """Recalcs the Demand by Population for Resources."""
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
        # need this to prevent type check problems
        log = self.log
        if self.pop.population_pP_tr is None:
            raise ValueError("pop.population_pP_tr")
        self.demand_by_pop_total_pn_tc.array = (
            self.demand_by_pop_per_person_pn_uc.array.T
            * self.pop.population_pP_tr.df["Size"].to_numpy().T
        ).T
        log.debug(f"{self.demand_by_pop_total_pn_tc.df=}")
        test = np.einsum(
            "pn,p->pn",
            self.demand_by_pop_per_person_pn_uc.array,
            self.pop.population_pP_tr.df["Size"].to_numpy(),
        )
        log.debug(f"{test=}")
        if not np.array_equal(self.demand_by_pop_total_pn_tc.array, test):
            breakpoint()
            log.critical("einsum fails!")

    def set_demand_by_popsum1_per_person_p1n_uc(self):
        """Recalcs the Demand by Population Summary Level 1 for Resources."""
        log = self.log
        # Original math put the level or popsum1 data here now move to
        # population
        # self.level_demand_ln_df = np.array(self.level_pl_df).T @ np.array(
        #     self.demand_pn_df
        # )
        if self.pop.pop_to_popsum1_per_unit_map_pp1_us is None:
            raise ValueError("pop.pop_to_popsum1_per_unit_map_pp1_us")
        # then add to them

        self.demand_by_popsum1_per_person_p1n_uc.array = (
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array.T
            @ self.demand_by_pop_per_person_pn_uc.array
        )
        log.debug(f"{self.demand_by_popsum1_per_person_p1n_uc.df=}")
        # Einsum equivalent of the above, we use x since index needs to be a
        # single character
        breakpoint
        test = np.einsum(
            "px,pn->xn",
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_per_person_pn_uc.array,
        )
        log.debug(f"{test=}")
        if not np.array_equal(
            self.demand_by_popsum1_per_person_p1n_uc.array, test
        ):
            log.debug("einsum fails!")

    def set_demand_by_popsum1_total_p1n_tc(self):
        """Recalcs the Demand by Population Level 1 for Total Resource."""
        log = self.log
        # TODO: Eventually we will want to calculate this iteration
        # across all summaries so p -> p1 -> p2...
        # We need a general function that knows how to walk
        # a series of transforms so you feed it any point and it knows how to
        # get to any other level
        # Original math
        # self.level_total_demand_ln_df = (
        #    self.level_pl_df.T @ self.total_demand_pn_df
        # )
        self.demand_by_popsum1_total_p1n_tc.array = (
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array.T
            @ self.demand_by_pop_total_pn_tc.array
        )
        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        test = np.einsum(
            "px,pn->xn",
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_total_pn_tc.array,
        )
        if not np.array_equal(self.demand_by_popsum1_total_p1n_tc.array, test):
            log.debug("einsum fails f{self.demand_by_popsum1_total_p1n_tc=}")

        log.debug("for future calculate a dummy range version")
        # https://stackoverflow.com/questions/32171917/copy-2d-array-into-3rd-dimension-n-times-python
        # repeat along the first axis
        self.demand_by_popsum1_total_rp1n_tc.array = np.repeat(
            self.demand_by_popsum1_total_p1n_tc.array[np.newaxis, ...],
            self.demand_by_popsum1_total_rp1n_tc.array.shape[0],
            axis=0,
        )

    def set_demand_by_popsum1_total_cost_p1n_xc(self):
        """Recalc the total cost of demand by Population Level 1."""
        # log = self.log
        # original formula
        # self.level_total_cost_ln_df = (
        #       self.level_total_demand_ln_df * cost_ln_df.values)
        log = self.log
        if self.res.res_by_popsum1_cost_per_unit_p1n_us is None:
            raise ValueError("res_by_popsum1_cost_per_unit_p1n_us")
        self.demand_by_popsum1_total_cost_p1n_xc.array = (
            self.demand_by_popsum1_total_p1n_tc.array
            * self.res.res_by_popsum1_cost_per_unit_p1n_us.array
        )
        # TODO: the einsum is broken
        test = np.einsum(
            "xn,xn->xn",
            self.demand_by_popsum1_total_p1n_tc.array,
            self.res.res_by_popsum1_cost_per_unit_p1n_us.array,
        )
        if not np.array_equal(
            self.demand_by_popsum1_total_cost_p1n_xc.array, test
        ):
            log.critical(
                f"einsum fail f{self.demand_by_popsum1_total_p1n_tc=}"
            )
