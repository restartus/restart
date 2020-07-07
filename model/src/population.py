"""Population class.

Main the class
"""

# Note that pip install data-science-types caused errors
from typing import List
import numpy as np  # type:ignore
import pandas as pd  # type:ignore
from base import Base
from model import Model

import logging  # noqa: F401

# The default logger if you don't get a root logger
log = logging.getLogger(__name__)
log.debug("In %s", __name__)


class Population(Base):
    """Population objects are created here.

    It has a default model in it for testing which is the Bharat model
    You should override it with a new child class

    Population statistics and model for population
    Initially this containes population of p x 1
    Later it will be p x d where d are the detail columns
    For instance the number of covid patients
    The number of trips or visits or runs for a given population

    The second matrix p population describes is how to map population to:w

    l demand levels to give a p x l. Long term this becomes d x p x l
    So that you can have a different run rate for each detail d of population

    How are resources consumed by different levels in a population
    This is the key first chart in the original model.
    It takes a set of l protection levels and then for each of n resources,
    provides their burn rate. So it is a dataframe that is l x n

    In this first version, burn rates are per capita, that is per person in a
    given level.

    In a later version, we will allow different "burn rates" by population
    attributes so this becomes a 3 dimensional model. For convenience, the
    Frame object we have retains objects in their simple dataframe form since
    it is easy to extract

    For multidimenstional indices, we keep both the n-dimensional array
    (tensor) and also have a method ot convert it to a multiindex for use by
    Pandas

    There is a default mode contained here for testing, you should override
    this by creating a child class and overriding the init

    We also create a friendly name and long description as document strings
    eventually this will become a file we read in that is a data description
    but for now it is a dictionary
    """

    # These are the default structures
    attr_pd_arr = np.array([735.2, 7179.6])
    level_pm_arr = np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
    )

    res_demand_mn_arr = np.array(
        [[0, 1], [0, 2], [0, 2], [0.1, 3], [0.2, 4], [0.3, 6], [1.18, 0]]
    )

    # No need for initialization get it from model.data
    #        attr_pd_df: Optional[pd.DataFrame] = None,
    #        level_pm_df: Optional[pd.DataFrame] = None,
    #        res_demand_mn_df: Optional[pd.DataFrame] = None,
    #        level_pl_df: Optional[pd.DataFrame] = None,
    def __init__(
        self, model: Model,
    ):
        """Initialize all variables.

        All initialization here
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        # to pick up the description
        super().__init__()

        # create a sublogger if a root exists in the model
        if model.log_root is not None:
            log = self.log = model.log_root.log_class(self)

        # set the arrays of values should be a column vector
        # https://kite.com/python/answers/how-to-make-a-numpy-array-a-column-vector-in-python
        # A shortcut
        self.attr_pd_arr = model.data["Population p"]["Attributes pd"]
        self.attr_pd_df = pd.DataFrame(
            self.attr_pd_arr,
            index=model.label["Population p"],
            columns=model.label["Pop Detail d"],
        )
        log.debug(f"{self.attr_pd_df=}")

        self.set_description(
            model,
            f"{self.attr_pd_df=}",
            model.description["Population p"]["Attributers pd"],
        )

        # set the population by demand levels
        self.level_pm_arr = model.data["Population p"]["Protection m"]
        self.level_pm_df = pd.DataFrame(
            self.level_pm_arr,
            index=model.label["Population p"],
            columns=model.label["Protection Category m"],
        )
        log.debug(f"{self.level_pm_df=}")
        self.set_description(
            model,
            f"{self.level_pm_df=}",
            model.description["Population p"]["Protection Category m"],
        )

        # note these are defaults for testing
        # this is the protection level and the burn rates for each PPE
        self.res_demand_mn_arr = model.data["Population p"][
            "Protection Demand mn"
        ]
        self.res_demand_mn_df = pd.DataFrame(
            self.res_demand_mn_arr,
            index=model.label[" Level n"],
            columns=model.label["Protection Demand mn"],
        )
        log.debug(f"{self.res_demand_mn_df=}")
        # for compatiblity both the model and the object hold the same
        # description
        self.set_description(
            model,
            f"{self.res_demand_mn_df=}",
            model.description["Population p"]["Protection Demand mn"],
        )

        self.demand_pn_df = self.level_pm_df @ self.res_demand_mn_df
        log.debug(f"{self.demand_pn_df=}")
        self.set_description(
            model,
            f"{self.demand_pn_df=}",
            model.description["Population p"]["Population Demand pn"],
        )

        # now get the conversion from the many p populations to the much
        # smaller l levels that are easier to understand
        self.level_pl_arr = model.data["Population p"]["Pop to Level pl"]
        self.level_pl_df = pd.DataFrame(
            self.level_pl_arr,
            index=model.label["Population p"],
            columns=model.label["Pop Level l"],
        )
        log.debug(f"{self.level_pl_df=}")
        self.set_description(
            model,
            f"{self.level_pl_df=}",
            model.description["Population p"]["Pop to Level pl"],
        )

        self.level_demand_ln_df = self.level_pl_df.T @ self.demand_pn_df
        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
            model,
            f"{self.level_demand_ln_df=}",
            model.description["Population p"]["Level Demand ln"],
        )

        # now to the total for population
        # TODO: eventually demand will be across pdn so
        # across all the values
        self.total_demand_pn_df = (
            self.demand_pn_df * self.attr_pd_df["People"].values
        )
        log.debug(f"{self.total_demand_pn_df=}")
        # convert to demand by levels note we have to transpose
        self.set_description(
            model,
            f"{self.total_demand_pn_df=}",
            model.description["Population p"]["Population Total Demand pn"],
        )

        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        log.debug(f"{self.level_total_demand_ln_df=}")
        self.set_description(
            model,
            f"{self.level_total_demand_ln_df=}",
            model.description["Population p"]["Level Total Demand ln"],
        )

        # set to null to make pylint happy and instatiate the variable
        self.level_total_cost_ln_df = None
        self.set_description(
            model,
            f"{self.level_total_cost_ln_df=}",
            model.description["Population p"]["Level Total Cost ln"],
        )

    def level_total_cost(self, cost_ln_df):
        """Calculate the total cost of resource for a population level.

        The total cost of resources
        """
        self.level_total_cost_ln_df = (
            self.level_total_demand_ln_df * cost_ln_df.values
        )
        log.debug("level_total_cost_ln_df\n%s", self.level_total_cost_ln_df)

    # this works because python is call by assignment
    # so immutables are call by value but mutales like dataframes and numpy
    # arrays are call by reference this isn't used anymore
    def set_dataframe(
        self,
        input_df: pd.DataFrame,
        default_arr: np.array,
        index: List[str] = None,
        columns: List[str] = None,
    ) -> pd.DataFrame:
        """Set the dataframe up.

        Does the setup
        """
        if input_df is None:
            log.debug(f"no input_df, using {default_arr=}")
            input_df = pd.DataFrame(default_arr, index=index, columns=columns,)
        return input_df, input_df.values
