"""The Inventory Model.

Reads from dictionary for defaults
"""

import confuse  # type: ignore

from log import Log
from inventory import Inventory
from data import Data


class InventoryDict(Inventory):
    """InventoryDict - manages inventory reads from dictionary."""

    def __init__(
        self, config: confuse.Configuration, log_root: Log = None,
    ):
        """Initialize the inventorys.

        Reads from the default config yaml files
        """
        # to pick up the description
        super().__init__(config, log_root=log_root)
        log = self.log
        log.debug(f"in {__name__}")

        self.inv_by_popsum1_parameters_ip1n_tp = Data(
            "inv_by_popsum1_parameters_ip1n_tp",
            config,
            log_root=log_root)
        log.debug(f"{self.inv_by_popsum1_parameters_ip1n_tp=}")
