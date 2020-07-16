"""Consumption Model.

Consumption modeling
"""
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from modeldata import ModelData
from util import Log
from typing import Optional
from population import Population
from resourcemodel import Resource


class Consumption(Base):
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
        data: ModelData,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
            # the sample code to move up the logging for a period
            log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
        self.log = log


        if pop is None:
            log.warning("Not implemented, if no pop passed, use model.data")
        if res is None:
            log.warning("Not implemented, if no res passed, use model.data")
        if type == "Mitre":
            log.debug("Use Mitre consumption")
        elif type == "Johns Hopkins":
            log.debug("Use JHU burn rate model")
        else:
            log.debug("For anything else use Washington data")

        # the same thing in a function less code duplication
        # note these are defaults for testing
        # this is the protection level and the burn rates for each PPE
        self.res_demand_mn_arr = data.value["Resource Demand mn"]
        self.res_demand_mn_df = set_dataframe(
            self.res_demand_mn_arr,
            data.label,
            index="Pop Protection m",
            columns="Resource n",
        )
        log.debug(f"{self.res_demand_mn_df=}")
        # for compatiblity both the model and the object hold the same
        # description
        self.set_description(
            f"{self.res_demand_mn_df=}", data.description["Res Demand mn"],
        )

        self.demand_pn_df = self.level_pm_df @ self.res_demand_mn_df
        log.debug(f"{self.demand_pn_df=}")
        self.demand_pn_df.index.name = "Population p"
        self.demand_pn_df.columns.name = "Resource n"
        self.set_description(
            f"{self.demand_pn_df=}",
            data.description["Population p"]["Population Demand pn"],
        )

        self.level_demand_ln_df = self.level_pl_df.T @ self.demand_pn_df
        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
            f"{self.level_demand_ln_df=}",
            data.description["Population p"]["Level Demand ln"],
        )
        # now to the total for population
        # TODO: eventually demand will be across pdn so
        # across all the values
        self.total_demand_pn_df = (
            self.demand_pn_df * self.attr_pd_df["Size"].values
            # self.demand_pn_df
            # * self.attr_pd_arr
        )
        log.debug(f"{self.total_demand_pn_df=}")
        # convert to demand by levels note we have to transpose
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
        # set to null to make pylint happy and instatiate the variable
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

        # method chaining
        return self
