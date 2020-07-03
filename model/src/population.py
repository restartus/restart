"""
Population class.
Main the class
"""

# Note that pip install data-science-types caused errors
import numpy as np  # type:ignore
import pandas as pd  # type:ignore
from base import Base
from model import Model

import logging
from util import setLogger

log = setLogger(__name__)
log.debug("In %s", __name__)


class Population(Base):
    """
    Population objects are created here.

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

    def __init__(
        self,
        model: Model,
        attr_pd_df: pd.DataFrame = None,
        protection_pm_df: pd.DataFrame = None,
        res_demand_mn_df: pd.DataFrame = None,
        level_pl_df: pd.DataFrame = None,
    ):
        """Initialize all variables.
        All initialization here
        """

        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        # to pick up the description
        super().__init__()

        # set the arrays of values should be a column vector
        # https://kite.com/python/answers/how-to-make-a-numpy-array-a-column-vector-in-python
        # A shortcut
        if attr_pd_df is None:
            attr_pd_arr = np.array([735.2, 7179.6])
            attr_pd_df = pd.DataFrame(
                attr_pd_arr,
                index=model.label["Population"],
                columns=model.label["Pop Detail"],
            )

        self.attr_pd_df = attr_pd_df
        log.debug("self.attr_pd\n%s", self.attr_pd_df)

        self.setDescription(
            model,
            f"{attr_pd_df=}".split("=")[0],
            """
## Population Details (pd)
There are p Populations in the model and each population
can have d details about them such as their degree of age,
ethnicity, attitudes and awareness behaviors
         """,
        )

        # set the population by demand levels
        if protection_pm_df is None:
            protection_pm_arr = np.zeros((model.dim["p"], model.dim["m"]))
            protection_pm_arr[0, -1] = 0.5
            protection_pm_arr[0, -2] = 0.5
            protection_pm_arr[1, 1] = 1.0
            log.debug("protection_pm_arr %s", protection_pm_arr)
            protection_pm_df = pd.DataFrame(
                protection_pm_arr,
                index=model.label["Population"],
                columns=model.label["Pop Protection"],
            )
        # https://docs.python.org/3/library/pdb.html
        self.protection_pm_df = protection_pm_df
        log.debug("self.protection_pm_df %s", self.protection_pm_df)
        self.setDescription(
            model,
            f"{self.protection_pm_df=}".split("=")[0],
            """
## Population Protection Level (pm)
There are p Populations in the model and each protection
level for the burn rates
                   """,
        )

        # note these are defaults for testing
        # this is the protection level and the burn rates for each PPE
        if res_demand_mn_df is None:
            res_demand_mn_arr = np.array(
                [
                    [0, 1],
                    [0, 2],
                    [0, 2],
                    [0.1, 3],
                    [0.2, 4],
                    [0.3, 6],
                    [1.18, 0],
                ]
            )
            log.debug("res_demand_mn_arr %s", res_demand_mn_arr)
            res_demand_mn_df = pd.DataFrame(
                res_demand_mn_arr,
                index=model.label["Pop Protection"],
                columns=model.label["Resource"],
            )
        self.res_demand_mn_df = res_demand_mn_df
        # for compatiblity both the model and the object hold the same
        # description
        self.setDescription(
            model,
            f"{res_demand_mn_df=}".split("=")[0],
            """
        ## Population demand for Resources (mn)
        The burn rates per capita for resources

        For example, 1.18 would mean you need 1.18 N95 masks per day for a
        given population
        """,
        )

        self.demand_pn_df = self.protection_pm_df @ self.res_demand_mn_df
        log.debug("population.demand_pn_df %s", self.demand_pn_df)

        self.setDescription(
            model,
            f"{self.demand_pn_df=}".split("=")[0],
            """
        ## Population demand
        This is the total demand for a give population so this is not the per
        capita demand but the demand for an entire population row
        """,
        )

        # now get the conversion from the many p populations to the much
        # smaller l levels that are easier to understand
        if level_pl_df is None:
            assert model.dim["p"] == model.dim["l"]
            level_pl_df = pd.DataFrame(
                np.eye((model.dim["p"])),
                index=model.label["Population"],
                columns=model.label["Pop Level"],
            )
        self.level_pl_df = level_pl_df
        log.debug("level_pl_df\n%s", self.level_pl_df)

        self.setDescription(
            model,
            f"{level_pl_df=}".split("=")[0],
            """
        ## Population's mapped into Protection or Summary Levels
        This maps every population p into any number of summary levels p
        summarized by the l Protection level used. In this model higher
        levels mean more protection by convention, but that isn't necessary.
        You can also a given population row spread across different levels
        so that for instance a percentage of a population could go into
        different rows
        """,
        )

        self.level_demand_ln_df = self.level_pl_df.T @ self.demand_pn_df
        name = "level_demand_ln_df"
        log.debug(f"{name}\n%s", self.level_demand_ln_df)

        self.setDescription(
            model,
            f"{self.level_demand_ln_df=}".split("=")[0],
            """
        ## Population Demand summarized by Summary or Protection Level
        This is the per capita demand for a set of n resources
        summarized by the l Protection level used. It provides a view of demand
        aggregated by the summary level
        """,
        )

        # now to the total for population
        self.total_demand_pn_df = (
            self.demand_pn_df * self.attr_pd_df["People"].values
        )
        log.debug("total_demand_pn_df\n%s", self.total_demand_pn_df)
        # convert to demand by levels note we have to transpose
        self.setDescription(
            model,
            f"{self.total_demand_pn_df=}".split("=")[0],
            """
        ## Population Demand by P Population categories
        This is the per capita demand for a set of n resources
        for all p Population levels.
        """,
        )

        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        log.debug(
            "level_total_demand_ln_df\n%s", self.level_total_demand_ln_df
        )
        self.setDescription(
            model,
            f"{self.level_total_demand_ln_df=}".split("=")[0],
            """
        ## Population Demand by L Summary Levels
        This is the per capita demand for a set of n resources
        that is summarize by the L protection levels.
        """,
        )

        # set to null to make pylint happy and instatiate the variable
        self.level_total_cost_ln_df = None
        self.setDescription(
            model,
            f"{self.level_total_cost_ln_df=}".split("=")[0],
            """
        ## Population Demand Total Cost by N Summary Levels
        This is the total cost for a set of n resources
        that is summarize by the L protection levels.
        """,
        )

    def level_total_cost(self, cost_ln_df):
        """Calculate the total cost of resource for a population level
        """
        self.level_total_cost_ln_df = (
            self.level_total_demand_ln_df * cost_ln_df.values
        )
        log.debug("level_total_cost_ln_df\n%s", self.level_total_cost_ln_df)
