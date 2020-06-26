"""
Population class
Main the class
"""
import logging
import numpy as np
import pandas as pd

LOG = logging.getLogger(__name__)
LOG.debug('In %s', __name__)


class Population:
    """ Population objects are created here
    It has a default model in it for testing which is the Bharat model
    You should override it with a new child class

    Population statistics and model for population
    Initially this containes population of p x 1
    Later it will be p x d where d are the detail columns
    For instance the number of covid patients
    The number of trips or visits or runs for a given population

    The second matrix p population describes is how to map population to
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
    """

    def __init__(self, model):

        # set the arrays of values
        self.attr_pd_arr = np.array([735.2, 7179.6])
        self.attr_pd_df = pd.DataFrame(self.attr_pd_arr,
                                       index=model.label['Population'],
                                       columns=model.label['Pop Details'])
        LOG.debug('pop_levels, p x d %s', self.attr_pd_arr.shape)

        # set the population by demand levels
        self.level_pl_arr = np.zeros((model.dim['p'],
                                      model.dim['l']))
        self.level_pl_arr[0, -1] = 0.5
        self.level_pl_arr[0, -2] = 0.5
        self.level_pl_arr[1, 1] = 1.0
        # https://docs.python.org/3/library/pdb.html
        LOG.debug('pop.level_pl_arr %s', self.level_pl_arr.shape)

        self.level_pl_df = pd.DataFrame(self.level_pl_arr,
                                        index=model.label['Population'],
                                        columns=model.label['Level'])

        # note these are defaults for testing
        self.level_demand_ln_arr = np.array([[0, 0],
                                             [0, 1],
                                             [0, 2],
                                             [0.1, 3],
                                             [0.2, 4],
                                             [0.3, 6],
                                             [1.18, 0]])

        self.level_demand_ln_df = pd.DataFrame(self.level_demand_ln_arr,
                                               columns=model.label["Level"],
                                               index=model.label["Resource"])

        self.demand_pn_df = self.level_pl_df @ model.level_demand_ln_df

        # now to the total for population
        self.total_demand_pn_df = self.demand_pn_df * self.attr_pd_df["People"].values

        # convert to demand by levels note we have to transpose
        self.level_total_demand_ln_df = self.level_pl_df.T @ self.total_demand_pn_df
        LOG.debug('population by level total demand %s',
                  self.level_total_demand_ln_df)
