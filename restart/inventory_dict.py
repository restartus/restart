"""The Inventory Model.

Reads from dictionary for defaults
"""

import confuse  # type: ignore

from inventory import Inventory
from log import Log


class InventoryDict(Inventory):
    """InventoryDict - manages inventory reads from dictionary."""

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
    ):
        """Initialize the inventorys.

        Reads from the default config yaml files
        """
        # The default is read from the dictionary
        super().__init__(config, log_root=log_root)
        log = self.log
        log.debug(f"in {__name__}")
