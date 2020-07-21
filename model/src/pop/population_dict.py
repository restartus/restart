"""Population Data Read.

Read in the population from the model dictionary
"""
import logging
import numpy as np  # type: ignore
import pandas as pd  # type: ignore # noqa: F401
# import numpy as np  # type: ignore
# https://www.python.org/dev/peps/pep-0420/
# in this new version we cannot depend on Model to be preformed
# from model import Model
from typing import Optional, Dict
from util import Log, set_dataframe
from population import Population
from modeldata import ModelData


class PopulationDict(Population):
    """Population Data Readers.

    Reads the population data. The default is to read from the model.data
    """

    def __init__(
        self,
        data: ModelData,
        label: Dict,
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
        super().__init__(log_root=log_root)

        # create a sublogger if a root exists in the model
        if log_root is not None:
            self.log_root: Log = log_root
            log = log_root.log_class(self)
            # breakpoint()
            log.debug(f"{log_root=}, {log_root.con=}")
            self.log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            self.log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
            log.debug(f"no log_root using {log=}")
        self.log = log

        # type declarations
        self.attr_pd_arr: np.ndarray
        self.attr_pd_df: pd.DataFrame
        self.level_pm_arr: np.ndarray
        self.level_pm_labs: list

        if label is None:
            raise ValueError(f"{label=} is null")

        # get population data
        self.attr_pd_arr = np.array(
                data.value["Population p"]["Pop Detail Data pd"]['Size'])
        self.attr_pd_df = set_dataframe(
            self.attr_pd_arr,
            label=label,
            index=index,
            columns=columns)
        log.debug(f"{self.attr_pd_arr=}")

        # get mapping data
        self.level_pm_arr = np.array(
                data.value["Population p"]["Protection pm"])
        self.level_pm_labs = list(data.label["Population p"])
        self.level_pm_df = pd.DataFrame(
                self.level_pm_arr,
                index=self.level_pm_labs,
                columns=data.label["Consumption m"])
        log.debug(f"{self.level_pm_df=}")
        self.set_description(
                f"{self.level_pm_df=}",
                data.description['Population p']['Protection pm'])
        log.debug(f"{self.description['level_pm_df']=}")
