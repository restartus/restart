"""Population Data Read.

Read in the population from the model dictionary
"""
import logging

# import numpy as np  # type: ignore
# https://www.python.org/dev/peps/pep-0420/
# in this new version we cannot depend on Model to be preformed
# from model import Model
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from population import Population
from util import Log, set_dataframe


class PopulationDict(Population):
    """Population Data Readers.

    Reads the population data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        # TODO: unify indexing across classes
        index: Optional[str] = None,
        columns: Optional[str] = None,
        log_root: Log = None,
        type: str = None,
    ):
        """Initialize the population object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(config, log_root=log_root)

        # create a sublogger if a root exists in the model
        if log_root is not None:
            self.log_root: Log = log_root
            log = log_root.log_class(self)
            log.debug(f"{log_root=}, {log_root.con=}")
            self.log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            self.log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
            log.debug(f"no log_root using {log=}")
        self.log = log

        # type declarations
        self.detail_pd_arr: np.ndarray
        self.detail_pd_df: pd.DataFrame
        self.level_pm_arr: np.ndarray

        if config is None:
            raise ValueError(f"{config=} is null")

        # get population data
        # TODO: Only gets the size, long term need all addributes
        self.detail_pd_arr = np.array(
            config["Data"]["Population p"]["Pop Detail Data pd"]["Size"].get()
        )
        self.detail_pd_df = set_dataframe(
            self.detail_pd_arr,
            label=config["Label"].get(),
            index=index,
            columns=columns,
        )
        log.debug(f"{self.detail_pd_arr=}")
        self.set_description(
            f"{self.detail_pd_df=}",
            config["Description"]["Population p"]["Pop Detail pd"].get(),
        )
        log.debug(f"{self.description['detail_pd_df']=}")

        # get mapping data
        self.level_pm_arr = np.array(
            config["Data"]["Population p"]["Protection pm"].get()
        )
        self.level_pm_df = set_dataframe(
            self.level_pm_arr,
            label=config["Label"].get(),
            index="Population p",
            columns="Demand m",
        )
        log.debug(f"{self.level_pm_df=}")
        self.set_description(
            f"{self.level_pm_df=}",
            config["Description"]["Population p"]["Protection pm"].get(),
        )
        log.debug(f"{self.description['level_pm_df']=}")

        self.level_pm_labs = config["Label"]["Population p"].get()
