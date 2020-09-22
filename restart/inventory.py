"""The Inventory Model.

What inventory are and how they are consumed
"""
# allows return self typing to work
from __future__ import annotations

# For slices of parameters
from typing import Callable, Optional

import confuse  # type: ignore
import numpy as np  # type: ignore

from base import Base  # type: ignore
from data import Data, DataDict
from log import Log  # type: ignore
from util import round_up

# https://docs.python.org/3/library/enum.html


class Inventory(Base):
    """Inventory - Manages all the inventories that are used in the model.

    This calculates the actually inventory of resources the key variable using
    a simple EOQ model. It is a DataDict so here are the key elements:

    inv_by_popsum1_param_rp1n_tp - The major parameters for this
    - min_inv - Minimum inventory (in total units)
    - min_period - The inventory desired (in days of average demand)
    - initial - Initial inventory
    - min_order - The order size to suppliers (can be EOQ or just a simple min)

    These are estimated by:
        Range r - A range of estimates for each
        Population Summary 1 - For each summarized population level
        Resource - Each resource

    Output:

    inv_by_popsum1_total_tgrDp1n_tc  -  The main return is a tensor:
        Time t - timeline
        Geolocation g - The location
        Range r - The range of backstops with inventory
        Population Summary 1 - Summary level
        Resource n - Resources stocked

    Internal Variables:
        - Dynamically set and used in period to minimum demand calculation
            self.inv_average_orders_by_popsum1_per_period_rp1n_uf

    Methods:
    self.inv_order_by_popsum1_total_trgDp1n_tc
    This is a simple minimum order model so the main methods are:

    set_average_orders_per_period - Set the average demand per day so that

    Each of these methods changes the ordering. Note that in a time based model
    this changes significantly since we are not doing a period.

    So what we get is a `order` which is a vector over time of order quantities
    for instance two periods of orders for 12 and then 34 units the next day.
    And we have a range where the orders could be twice as high
        [[12, 34], [24, 68]]


    Methods:
    This is a simple model that changes the inventory level.

    - set_min - The minimum stocking level so that the inventory stays above a
    minimum level
    - order -    kjj
    - supply_order - Request from suppliers (round up to min_order_quantity aka
      eoq)
    - round_up_to_min_order - Round up the supply order to the minimum
    - fulfill - Send product to demanders
    """

    def __init__(
        self,
        read_data_fn: Callable[
            [Inventory, confuse.Configuration, Optional[Log]], None
        ],
        config: confuse.Configuration,
        log_root: Log = None,
    ):
        """Initialize the Inventorys.

        Does a read in parameters
        """
        # initialize logging and description
        super().__init__(log_root=log_root)
        log = self.log
        self.config = config

        self.inv_by_popsum1_total_tgrDp1n_tc: Data
        self.inv_by_popsum1_param_grDp1n_tp: DataDict
        self.inv_leadtime_n_tp: Data

        # Helpers to handle period calculations
        self.inv_order_by_popsum1_total_trgDp1n_tc: Data
        self.inv_cum_orders_by_popsum1_total_tgrDp1n_tc: Data
        self.inv_supply_order_by_popsum1_total_tgrD1p1n_tc: Data
        self.inv_supply_fulfill_by_popsum1_total_tgrDp1n_tc: Data

        self.inv_average_orders_by_popsum1_per_period_grDp1n_uf: Data

        # instead of classes to read data we just use a callback
        self.read_data_fn = read_data_fn
        log.debug(f"Calling {read_data_fn=}")
        self.read_data_fn(self, config, log_root)

    def order(self, order_by_popsum1_total_tgrDp1n_tc: Data) -> Inventory:
        """Order by Customer from Inventory.

        Take a new order that is a time vector. This assumes that each row of
        the population matrix is a customer population p in a given geography g
        that orders resources n. The quantity varies by the demand model D used
        and the range of values r.

        The logic
        We iteratively calculate from each of the returns where the next period
        inventory is and trick is that we cannot fulfill more than what we have
        in Inventory and what we can't fill becomes a backorder

        The Supply Order is a little tricky because we have a minimum buffer
        stock in inventory that we attempt to keep at all times. So when we dip
        below this, we order a little more to get us back to minimum inventory.
        The tricky part is that in prior periods, we may have Backfill orders
        so we need to track the cumulative backfills so we don't overorder


        Returns:
        Fulfillment vector. Now is the fulfillment across time, geo, model and
        range
        Backorders vector. What goes into backorder to be delivered later later
        Backfills vector. The orders needed to get back to minimum inventory
        levels
        """
        # simpler names
        order = order_by_popsum1_total_tgrDp1n_tc.array
        cum_orders = self.inv_cum_orders_by_popsum1_total_tgrDp1n_tc.array
        inv = self.inv_by_popsum1_total_tgrDp1n_tc.array
        backorders = self.inv_orders_by_popsum1_total_tgrDp1n_tc.array
        fulfill = self.inv_fulfill_by_popsum1_total_tgrDp1n_tc.array


        # Initialization to initial inventory and backorders are all zero
        inv[0] = self.inv_by_popsum1_param_grDp1n_tp.dict["initial"].array
        backorders[0].fill(0)

        for t in range(0, order.shape[0]):
            # get inventory from last time and calculate this time use the min
            # for the very start
            inv[t] = inv[min(t - 1, 0)] + self.supply_fulfilled(t)

            # add to the cumulative total demand
            cum_orders[t] = backorders[t-1] + order[t]

            # Now fulfill the entire demand with the existing inventory
            # as well as a minimum inventory that is used for buffering

            fulfill[t] = np.min(inv[t], cum_orders[t])

            # new inventory, and see what new backorders we have
            inv[t] = inv[t] - fulfill[t]
            backorders[t] = cum_orders[t] - fulfill[t]
            new_backorders[t] = np.max(backorders[t] - backorders[t-1], 0)

            supply_order[t] = round_up(new_backorders[t], inv_min)

        return self

    def supply_fulfilled(self, t: int) -> Inventory:
        """Fulfill supply order lagged by leadtime.

        A very simple standard leadtime for all resources
        """
        self.inv_supply_order_by_popsum1_total_tgrD1p1n_tc.array[
            min(t - self.inv_leadtime_n_tp.array, 0)
        ]
        return self
