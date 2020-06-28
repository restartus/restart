"""
Population class
Main the class
"""
from typing import Dict
import logging
import numpy as np
import pandas as pd

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
LOG.debug("In %s", __name__)


class Population:
    """ Population objects are created here
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
    eventually this will become a file we read in that is a data description but
    for now it is a dictionary
    """

    def __init__(
        self,
        model,
        attr_pd_df=None,
        protection_pm_df=None,
        prot_demand_mn_df=None,
        level_pl_df=None,
    ):

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
        model.description["population.attr_pd_df"] = '''
## Population Details pd
There are p Populations in the model and each population
can have d details about them such as their degree of age,
ethnicity, attitudes and awareness behaviors
                   '''
        LOG.debug("self.attr_pd\n%s", self.attr_pd_df)

        # set the population by demand levels
        if protection_pm_df is None:
            protection_pm_arr = np.zeros((model.dim["p"], model.dim["m"]))
            protection_pm_arr[0, -1] = 0.5
            protection_pm_arr[0, -2] = 0.5
            protection_pm_arr[1, 1] = 1.0
            LOG.debug("protection_pm_arr %s", protection_pm_arr)
            protection_pm_df = pd.DataFrame(
                protection_pm_arr,
                index=model.label["Population"],
                columns=model.label["Pop Protection"],
            )
        # https://docs.python.org/3/library/pdb.html
        self.protection_pm_df = protection_pm_df
        LOG.debug("self.protection_pm_df %s", self.protection_pm_df)

        # note these are defaults for testing
        # this is the protection level and the burn rates for each PPE
        if prot_demand_mn_df is None:
            prot_demand_mn_arr = np.array(
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
            LOG.debug("prot_demand_mn_arr %s", prot_demand_mn_arr)
            prot_demand_mn_df = pd.DataFrame(
                prot_demand_mn_arr,
                index=model.label["Pop Protection"],
                columns=model.label["Resource"],
            )
        self.prot_demand_mn_df = prot_demand_mn_df

        self.demand_pn_df = self.protection_pm_df @ self.prot_demand_mn_df
        LOG.debug("population.demand_pn_df %s", self.demand_pn_df)

        # now get the conversion from the many p populations to the much smaller
        # l levels that are easier to understand
        if level_pl_df is None:
            assert model.dim["p"] == model.dim["l"]
            level_pl_df = pd.DataFrame(
                np.eye((model.dim["p"])),
                index=model.label["Population"],
                columns=model.label["Pop Level"],
            )
        self.level_pl_df = level_pl_df
        LOG.debug("level_pl_df\n%s", self.level_pl_df)

        self.level_demand_ln_df = self.level_pl_df.T @ self.demand_pn_df
        LOG.debug("level_demand_ln_df\n%s", self.level_demand_ln_df)

        # now to the total for population
        self.total_demand_pn_df = (
            self.demand_pn_df * self.attr_pd_df["People"].values
        )
        LOG.debug("total_demand_pn_df\n%s", self.total_demand_pn_df)
        # convert to demand by levels note we have to transpose

        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        LOG.debug(
            "level_total_demand_ln_df\n%s", self.level_total_demand_ln_df
        )

        # set to null to make pylint happy
        self.level_total_cost_ln_df = None

    def level_total_cost(self, cost_ln_df):
        """Calculate the total cost of resource for a population level
        """
        self.level_total_cost_ln_df = (
            self.level_total_demand_ln_df * cost_ln_df.values
        )
        LOG.debug("level_total_cost_ln_df\n%s", self.level_total_cost_ln_df)
