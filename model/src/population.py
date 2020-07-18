"""Population class.

This is the base class for all models. It instantiates the population to be
filled in.

It also includes a default() for setting up the main attribute matrix,
attr_pd_arr and then a calc() which calculates the rest of the related data
"""

# Note that pip install data-science-types caused errors
from base import Base
from modeldata import ModelData

# Insert the classes of data we support here
from typing import Optional, Dict
from util import Log, set_dataframe
import numpy as np  # type:ignore
import pandas as pd  # type:ignore

# import pandas as pd  # type:ignore


import logging  # noqa: F401


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

    # https://satran.in/b/python--dangerous-default-value-as-argument
    # https://stackoverflow.com/questions/2…

    # These are the default structures
    # attr_pd_arr = np.array([735.2, 7179.6])
    # level_pm_arr = np.array(
    #     [
    #         [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5],
    #         [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    #     ]
    # )

    # res_demand_mn_arr = np.array(
    #     [[0, 1], [0, 2], [0, 2], [0.1, 3], [0.2, 4], [0.3, 6], [1.18, 0]]
    # )

    # No need for initialization get it from model.data
    #        attr_pd_df: Optional[pd.DataFrame] = None,
    #        level_pm_df: Optional[pd.DataFrame] = None,
    #        res_demand_mn_df: Optional[pd.DataFrame] = None,
    #        level_pl_df: Optional[pd.DataFrame] = None,
    def __init__(self, log_root: Log = None, config: Dict = None):
        """Initialize all variables.

        All initialization here and uses type to determine which method to call
        The default is PopulationDict which reads from the model.data
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        # to pick up the description
        super().__init__(log_root=log_root)
        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            # The default logger if you don't get a root logger
            log = logging.getLogger(__name__)
        self.log = log
        log.debug("In %s", __name__)

        self.attr_pd_arr: Optional[np.ndarray] = None
        self.attr_pd_df: Optional[pd.DataFrame] = None
        self.config: Optional[Dict] = config

    def default(self, data: ModelData):
        """Load The default method for getting values.

        Does the default pull from data.
        """
        # set the arrays of values should be a column vector
        # https://kite.com/python/answers/how-to-make-a-numpy-array-a-column-vector-in-python
        # A shortcut

        # this is superceded by set_dataframe
        # self.attr_pd_arr = data.value["Population p"]["Pop Detail Data pd"]
        # log.debug(f"{self.attr_pd_arr=}")
        # self.attr_pd_df = pd.DataFrame(
        #     self.attr_pd_arr,
        #     index=data.label["Population p"],
        #    columns=data.label["Pop Detail d"],
        # )
        # self.attr_pd_df.index.name = "Population p"
        # self.attr_pd_df.columns.name = "Pop Detail d"
        # log.debug(f"{self.attr_pd_df=}")
        # self.set_description(
        #    f"{self.attr_pd_df=}",
        #     data.description["Population p"]["Pop Detail pd"],
        # )
        # the same thing in a function less code duplication
        log = self.log
        self.attr_pd_arr = data.value["Population p"]["Pop Detail Data pd"]
        self.attr_pd_df = set_dataframe(
            self.attr_pd_arr,
            data.label,
            index="Population p",
            columns="Pop Detail d",
        )
        log.debug(f"{self.attr_pd_df=}")
        log.debug(f"{self.attr_pd_df.index.name=}")
        log.debug(f"{self.attr_pd_df.columns.name=}")
        self.set_description(
            f"{self.attr_pd_df=}",
            data.description["Population p"]["Pop Detail pd"],
        )

        # new population class, so it can be replaced in a class

        # not running for rich df is null
        # population_data_oes = PopulationOES(
        #     model,
        #     # source=model.data["Population p"]["Pop Detail Data pd"],
        #     index=model.label["Population p"],
        #     columns=model.label["Pop Detail d"],
        # )
        # log.debug(f"{population_data_oes=}")
        # log.debug(f"{population_data=}")

        # log.debug(f"{population_data.attr_pd_arr=}")
        # log.debug(f"{population_data.attr_pd_df=}")
        # if (
        #    population_data.attr_pd_arr is None
        #    or population_data.attr_pd_df is None
        # ):
        #     raise ValueError(
        #        f"no population data {population_data.attr_pd_arr=}"
        #    )
        # TODO: should we just instantiate PopDict or PopOES instead of this
        # shovelling of parameters
        # self.attr_pd_arr = population_data.attr_pd_arr
        # self.attr_pd_df = population_data.attr_pd_df
        log.debug(f"{self.attr_pd_df=}")
        self.set_description(
            f"{self.attr_pd_df=}",
            data.description["Population p"]["Pop Detail pd"],
        )
        log.debug(f"{self=}")
        log.debug(f"{self.description=}")
        log.debug(f"{self.description['attr_pd_df']=}")

    def calc(self, data: ModelData):
        """Run the calculations derived.

        TODO: should these go into the consumption class
        they are fundamentally about translating population
        into summary levels l for reporting

        And about translating it into consumption levels
        """
        # set the population by demand levels
        log = self.log

        # now get the conversion from the many p populations to the much
        # smaller l levels that are easier to understand
        self.level_pl_arr = data.value["Population p"]["Pop to Level pl"]
        self.level_pl_df = set_dataframe(
            self.level_pl_arr,
            data.label,
            index="Population p",
            columns="Pop Level l",
        )
        log.debug(f"{self.level_pl_df=}")
        self.set_description(
            f"{self.level_pl_df=}",
            data.description["Population p"]["Pop to Level pl"],
        )
