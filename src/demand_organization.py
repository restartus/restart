"""Demand Model.

Demand modeling
"""
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from demand import Demand
from log import Log
from organization import Organization
from resourcemodel import Resource


class DemandOrganization(Demand):
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
        org: Organization,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # initialize the data objects and logging
        super().__init__(config, res, pop=None, log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        self.recalc(org, res)

    def recalc(self, org, res):
        """Recalculate all demands.

        Right now it must be run in this order
        """
        self.set_demand_by_pop_per_person_pn_uc(org)
        self.set_demand_by_pop_total_pn_tc(org)
        self.set_demand_by_popsum1_per_person_p1n_uc(org)
        self.set_demand_by_popsum1_total_p1n_tc(org)
        self.set_demand_by_popsum1_total_cost_p1n_xc(res)

    def set_demand_by_pop_per_person_pn_uc(self, org):
        """Sets the Demand by Population Per Person."""
        log = self.log

        # original matrix multiply to get per person demands
        # self.demand_pn_arr = np.array(pop.level_pm_df) @ np.array(
        #     self.level_to_res_mn_df
        # )

        if org.org_demand_per_unit_map_od_um is None:
            raise ValueError("org.org_demand_per_unit_map_od_um")

        self.demand_by_pop_per_person_pn_uc.array = (
            org.org_demand_per_unit_map_od_um.array
            @ self.demand_per_unit_map_dn_um.array
        )

        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        # Einsum equivalent for automatic generation
        test = np.einsum(
            "pd,dn->pn",
            org.org_demand_per_unit_map_od_um.array,
            self.demand_per_unit_map_dn_um.array,
        )
        log.debug(f"{test=}")
        if np.array_equal(self.demand_by_pop_per_person_pn_uc.array, test):
            log.debug("einsum works!")

    def set_demand_by_pop_total_pn_tc(self, org):
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
        if org.organization_oO_tr is None:
            raise ValueError("pop.population_pP_tr")
        self.demand_by_pop_total_pn_tc.array = (
            self.demand_by_pop_per_person_pn_uc.array.T
            * org.organization_oO_tr.df["Employees"].to_numpy().T
        ).T
        log.debug(f"{self.demand_by_pop_total_pn_tc.df=}")
        test = np.einsum(
            "pn,p->pn",
            self.demand_by_pop_per_person_pn_uc.array,
            org.organization_oO_tr.df["Employees"].to_numpy(),
        )
        log.debug(f"{test=}")
        if np.array_equal(self.demand_by_pop_per_person_pn_uc.array, test):
            log.debug("einsum works!")

    def set_demand_by_popsum1_per_person_p1n_uc(self, org):
        """Recalcs the Demand by Population Summary Level 1 for Resources."""
        log = self.log
        # Original math put the level or popsum1 data here now move to
        # population
        # self.level_demand_ln_df = np.array(self.level_pl_df).T @ np.array(
        #     self.demand_pn_df
        # )
        if org.org_to_orgsum1_per_unit_map_oo1_us is None:
            raise ValueError("pop.pop_to_popsum1_per_unit_map_pp1_us")
        # then add to them

        self.demand_by_popsum1_per_person_p1n_uc.array = (
            org.org_to_orgsum1_per_unit_map_oo1_us.array.T
            @ self.demand_by_pop_per_person_pn_uc.array
        )
        log.debug(f"{self.demand_by_popsum1_per_person_p1n_uc.df=}")
        # Einsum equivalent of the above, we use x since index needs to be a
        # single character
        # TODO: the einsum is broken
        """
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
        """

    def set_demand_by_popsum1_total_p1n_tc(self, org):
        """Recalcs the Demand by Population Level 1 for Total Resource."""
        log = self.log
        # TODO: Eventually we will want to calculate this iteration
        # across all summaries so p -> p1 -> p2...
        # And do this in a function because demand for instance
        # should not have to know the population dimension
        # Original math
        # self.level_total_demand_ln_df = (
        #    self.level_pl_df.T @ self.total_demand_pn_df
        # )
        self.demand_by_popsum1_total_p1n_tc.array = (
            org.org_to_orgsum1_per_unit_map_oo1_us.array.T
            @ self.demand_by_pop_total_pn_tc.array
        )
        log.debug(f"{self.demand_by_pop_per_person_pn_uc.df=}")
        test = np.einsum(
            "px,pn->xn",
            org.org_to_orgsum1_per_unit_map_oo1_us.array,
            self.demand_by_pop_total_pn_tc.array,
        )
        if np.array_equal(self.demand_by_popsum1_total_p1n_tc.array, test):
            log.debug("einsum works!")

        log.debug("for future calculate a dummy range version")
        # https://stackoverflow.com/questions/32171917/copy-2d-array-into-3rd-dimension-n-times-python
        # repeat along the first axis
        self.demand_by_popsum1_total_rp1n_tc.array = np.repeat(
            self.demand_by_popsum1_total_p1n_tc.array[np.newaxis, ...],
            self.demand_by_popsum1_total_rp1n_tc.array.shape[0],
            axis=0,
        )

    def set_demand_by_popsum1_total_cost_p1n_xc(self, res):
        """Recalc the total cost of demand by Population Level 1."""
        # log = self.log
        # original formula
        # self.level_total_cost_ln_df = (
        #       self.level_total_demand_ln_df * cost_ln_df.values)
        if res.res_by_popsum1_cost_per_unit_p1n_us is None:
            raise ValueError("res_by_popsum1_cost_per_unit_p1n_us")
        self.demand_by_popsum1_total_cost_p1n_xc.array = (
            self.demand_by_popsum1_total_p1n_tc.array
            * res.res_by_popsum1_cost_per_unit_p1n_us.array
        )
        # TODO: the einsum is broken
        """
        test = np.einsum(
            "xn,xn->xn",
            self.demand_by_pop_total_pn_tc.array,
            res.res_by_popsum1_cost_per_unit_p1n_us.array,
        )
        if np.array_equal(self.demand_by_popsum1_total_cost_p1n_xc, test):
            log.debug("einsum works!")
        """
