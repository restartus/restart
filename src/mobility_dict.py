"""Mobility Data Read.

Read in the mobility from the model dictionary
"""

import confuse  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from .data import Data  # type: ignore
from .log import Log  # type: ignore
from .mobility import Mobility  # type: ignore


class MobilityDict(Mobility):
    """Mobility Data Readers.

    Reads the mobility data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
        type: str = None,
    ):
        """Initialize the mobility object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        # get mobility data
        # Using the new Lucas data class
        self.mobility_mM_pr = Data(
            "mobility_mM_pr",
            config,
            log_root=log_root,
        )
        log.critical(f"{self.mobility_mM_pr.df=}")
