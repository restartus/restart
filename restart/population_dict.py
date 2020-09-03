"""Population Data Read.

Read in the population from the model dictionary
"""

import confuse  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from data import Data
from log import Log
from population import Population


class PopulationDict(Population):
    """Population Data Readers.

    Reads the population data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
    ):
        """Initialize the population object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        # get population data
        # Using the new Lucas data class
        self.population_pP_tr = Data(
            "population_pP_tr",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.population_pP_tr=}")

        self.pop_demand_per_unit_map_pd_um = Data(
            "pop_demand_per_unit_map_pd_um",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.pop_demand_per_unit_map_pd_um=}")

        self.pop_to_popsum1_per_unit_map_pp1_us = Data(
            "pop_to_popsum1_per_unit_map_pp1_us",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.pop_to_popsum1_per_unit_map_pp1_us=}")
