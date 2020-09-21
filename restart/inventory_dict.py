"""Read from a dictionary the Inventory Data

Reads from dictionary for defaults as a Callback
"""

import logging

from confuse import Configuration  # type: ignore

from data import Data, DataDict
from inventory import Inventory  # type: ignore
from log import Log


def inventory_dict_read(inv: Inventory, config: Configuration, log_root: Log):
    """InventoryDict - manages inventory reads from dictionary.

    Reads from the default config yaml files
    """
    log: logging.Logger = log_root.log
    log.debug(f"in {__name__}")
    inv.inv_by_popsum1_total_tgrDp1n_tc = Data(
        f"{inv.inv_by_popsum1_total_tgrDp1n_tc=}",
        config,
        log_root=log_root,
    )
    inv.inv_by_popsum1_param_rp1n_tp = DataDict(
        f"{inv.inv_by_popsum1_param_rp1n_tp=}", config, log_root=log_root
    )
    log.debug(f"{inv.inv_by_popsum1_param_rp1n_tp=}")
    # Helpers to handle period calculations
    inv.inv_min_by_popsum1_in_periods_rp1n_pc = Data(
        "inv_min_by_popsum1_in_periods_rp1n_pc", config, log_root=log_root
    )
    inv.inv_average_orders_by_popsum1_per_period_rp1n_uf = Data(
        "inv_average_orders_by_popsum1_per_period_rp1n_uf",
        config,
        log_root=log_root,
    )
    inv.inv_order_by_popsum1_total_trgDp1n_tc = Data(
        "inv_order_by_popsum1_total_trgDp1n_tc", config, log_root=log_root
    )
