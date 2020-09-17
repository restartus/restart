"""The Inventory Model.

Reads from dictionary for defaults
"""

import confuse  # type: ignore

from inventory import Inventory  # type: ignore
from log import Log  # type: ignore
from data import Data, DataDict


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

        self.inv_by_popsum1_total_tgrDp1n_tc = Data(
            f"{self.inv_by_popsum1_total_tgrDp1n_tc=}", config, log_root=log_root
        )
        self.inv_by_popsum1_param_rp1n_tp = DataDict(
            f"{self.inv_by_popsum1_param_rp1n_tp=}", config, log_root=log_root
        )
        log.debug(f"{self.inv_by_popsum1_param_rp1n_tp.df=}")
        # Helpers to handle period calculations
        self.inv_min_by_popsum1_in_periods_rp1n_pc = Data(
            "inv_min_by_popsum1_in_periods_rp1n_pc", config, log_root=log_root
        )
        self.inv_average_orders_by_popsum1_per_period_rp1n_uf = Data(
            "inv_average_orders_by_popsum1_per_period_rp1n_uf",
            config,
            log_root=log_root,
        )
        self.inv_order_by_popsum1_total_rp1n_tc = Data(
            "inv_order_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )
        # can only set minimum once inv_min exists and order too
        self.set_min(self.inv_init_by_popsum1_total_rp1n_tc)
