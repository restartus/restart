"""Demand Model.

Demand modeling
"""
from typing import Dict, Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from base import Base  # type: ignore
from data import Data  # type: ignore
from log import Log  # type: ignore
from population import Population  # type: ignore
from resourcemodel import Resource  # type: ignore


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

    def adjust_burn(self, new_burn) -> self:
        """Adjust the burn rates."""
        self.demand_per_unit_map_xrdn_um.array = new_burn
        self.recalc()
        return self

    def set_data(self, config, log_root):
        """Instantiate the base data objects for inheritance purposes."""
        log = self.log

        self.demand_per_unit_map_xrdn_um = Data(
            "demand_per_unit_map_xrdn_um", config, log_root=log_root
        )
        log.debug(f"{self.demand_per_unit_map_xrdn_um.df=}")

        self.demand_by_pop_per_person_xrtgpn_uc = Data(
            "demand_by_pop_per_person_xrtgpn_uc", config, log_root=log_root
        )

        # need to instantiate variables first

        self.demand_pop_total_xrtgpn_tc = Data(
            "demand_pop_total_xrtgpn_tc", config, log_root=log_root
        )

        self.demand_by_popsum1_per_person_xrtgp1n_uc = Data(
            "demand_by_popsum1_per_person_xrtgp1n_uc",
            config,
            log_root=log_root,
        )

        self.demand_by_popsum1_total_xrtgp1n_tc = Data(
            "demand_by_popsum1_total_xrtgp1n_tc", config, log_root=log_root
        )

        self.demand_by_popsum1_total_cost_xrtgp1n_xc = Data(
            "demand_by_popsum1_total_cost_xrtgp1n_xc",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.demand_by_popsum1_total_cost_xrtgp1n_xc.df=}")

    def recalc(self) -> self:
        """Recalculate all demands.

        Right now it must be run in this order
        """
        return (
            self.set_demand_by_pop_per_person_xrtgpn_uc()
            .set_demand_pop_total_xrtgpn_tc()
            .set_demand_by_popsum1_per_person_xrtgp1n_uc()
            .set_demand_by_popsum1_total_xrtgp1n_tc()
            .set_demand_by_popsum1_total_cost_xrtgp1n_xc()
        )

    def set_demand_by_pop_per_person_xrtgpn_uc(self) -> self:
        """Sets the Demand by Population Per Person."""
        log = self.log

        # original matrix multiply to get per person demands
        # self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
        #     self.level_to_res_mn_df
        # )

        if self.pop.pop_demand_per_unit_map_pgrd_um is None:
            raise ValueError("pop.pop_demand_per_unit_map_rgpd_um")

        # This no longer works in a multidimensional world
        # self.demand_by_pop_per_person_pn_uc.array = (
        # self.pop.pop_demand_per_unit_map_pd_um.array
        # @ self.demand_per_unit_map_dn_um.array
        # )
        # log.debug(f"{self.demand_by_pop_per_person_rtgpn_uc.df=}")
        # Einsum equivalent for automatic generation
        self.demand_by_pop_per_person_xrtgpn_uc.array = np.einsum(
            "rgpd,xrdn->xrptn",
            self.pop.pop_demand_per_unit_map_rgpd_um.array,
            self.demand_per_unit_map_xrdn_um.array,
        )
        log.debug(f"{self.demand_by_pop_per_person_xrtgpn_uc.array=}")
        return self

    def set_demand_pop_total_xrtgpn_tc(self) -> self:
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
        if self.pop.population_rpP_tr is None:
            raise ValueError("pop.population_rpP_tr")
        self.demand_pop_total_xrtgpn_tc.array = (
            self.demand_by_pop_per_person_xrtgpn_uc.array.T
            * self.pop.population_rpP_tr.df["Size"].to_numpy().T
        ).T
        self.demand_pop_total_xrtgpn_tc.array = np.einsum(
            "xrtgpn,rp->xrtgpn",
            self.demand_by_pop_per_person_xrtgpn_uc.array,
            self.pop.population_rpP_tr.df["Size"].to_numpy(),
        )
        return self

    def set_demand_by_popsum1_per_person_xrtgp1n_uc(self) -> self:
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

        # the matrix math only works in 2D
        # self.demand_by_popsum1_per_person_p1n_uc.array = (
        # self.pop.pop_to_popsum1_per_unit_map_pp1_us.array.T
        # @ self.demand_by_pop_per_person_pn_uc.array
        # )
        # Einsum equivalent of the above, we use x since index needs to be a
        # single character
        self.demand_by_popsum1_per_person_xrtgp1n_uc = np.einsum(
            "pz,rtgpn->xrtgzn",
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_per_person_xrtgpn_uc.array,
        )
        log.debug(f"{self.demand_by_popsum1_per_person_xrtgp1n_uc.df=}")
        return self

    def set_demand_by_popsum1_total_xrtgp1n_tc(self) -> self:
        """Recalcs the Demand by Population Level 1 for Total Resource."""
        log = self.log
        # TODO: Convert to only doing by _pop and then output do the summarization
        # This only works in 2-D
        # self.demand_by_popsum1_total_p1n_tc.array = (
        # self.pop.pop_to_popsum1_per_unit_map_pp1_us.array.T
        # @ self.demand_pop_total_pn_tc.array
        # )
        self.demand_by_popsum1_total_xrtgp1n_tc.array = np.einsum(
            "pz,xrtgpn->xrtgzn",
            self.pop.pop_to_popsum1_per_unit_map_pp1_us.array,
            self.demand_by_pop_total_xrtgpn_tc.array,
        )
        return self

    def set_demand_by_popsum1_total_cost_xrtgp1n_xc(self) -> self:
        """Recalc the total cost of demand by Population Level 1."""
        # log = self.log
        # original formula
        # self.level_total_cost_ln_df = (
        #       self.level_total_demand_ln_df * cost_ln_df.values)
        log = self.log
        if self.res.res_by_popsum1_cost_per_unit_pr1n_us is None:
            raise ValueError("self.res_by_popsum1_cost_per_unit_p1n_us")
        self.demand_by_popsum1_total_cost_rtgp1n_xc.array = (
            self.demand_by_popsum1_total_xrtgp1n_tc.array
            * self.res.res_by_popsum1_cost_per_unit_rp1n_us.array
        )
        test = np.einsum(
            "xrtgzn,zn->zn",
            self.demand_by_popsum1_total_xrtgp1n_tc.array,
            self.res.res_by_popsum1_cost_per_unit_p1n_us.array,
        )
        if not np.array_equal(
            self.demand_by_popsum1_total_cost_xrtgp1n_xc.array, test
        ):
            log.critical(
                f"einsum fail f{self.demand_by_popsum1_total_rtgp1n_tc=}"
            )
        return self
