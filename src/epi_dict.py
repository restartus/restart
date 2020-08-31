"""Epi Data Read.

Read in the epi from the model dictionary
"""

import confuse  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from data import Data
from epi import Epi
from log import Log


class EpiDict(Epi):
    """Epi Data Readers.

    Reads the epi data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
        type: str = None,
    ):
        """Initialize the epi object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        # get epi data
        # Using the new Lucas data class
        self.epi_eE_pr = Data(
            "epi_eE_pr",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.epi_eE_pr.df=}")
