"""The Inventory Model.

What inventory are and how they are consumed
"""
# allows return self typing to work
from __future__ import annotations

# For slices of parameters
from enum import Enum
from typing import List, Union

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from base import Base
from data import Data
from log import Log
from util import set_dataframe


# https://docs.python.org/3/library/enum.html
# These are the slices used
class InvParameter(Enum):
    """List positions in Inventory Parameter List."""

    INV_INITIAL = 0
    INV_EOQ = 1
    INV_MIN = 2


class Inventory(Base):
    """Inventory - Manages all the inventorys that are used in the model."""

    def __init__(
        self, config: confuse.Configuration, log_root: Log = None,
    ):
        """Initialize the Inventorys.

        Does a read in parameters
        """
        # initialize logging and description
        super().__init__(log_root=log_root)
        log = self.log
        self.config = config
        log.debug(f"in {__name__}")

        self.in_stock_p1n_df: pd.DataFrame
        # In the new world parameters are kept in a tuple
        self.inv_by_popsum1_parameters_ip1n_tp: List[Data]
        self.inv_min_in_periods_rp1n_arr: np.ndarray

    def set_inv_min(
        self,
        demand_per_period_p1n_df: pd.DataFrame,
        periods_rp1n: Union[np.ndarray, int],
    ) -> Inventory:
        """Set the minimum inventory in periods_r.

        A helper function that sets the minimum inventory
        Based on how many periods_r (days) you want stored

        TODO: This uses the range attribute so that you could set and
        inventory range of minimums
        """
        log = self.log
        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        if type(periods_rp1n) is int:
            log.debug(f"{periods_rp1n=} scalar inventory")
            # note we need r=1 for this to work so we insert an empty dimension
            # https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html
            self.inv_min_in_periods_rp1n_arr = periods_rp1n * np.ones_like(
                demand_per_period_p1n_df
            )
            self.inv_min_in_periods_rp1n_arr = np.expand_dims(
                self.inv_min_in_periods_rp1n_arr, axis=0
            )
        else:
            self.inv_min_in_periods_rp1n_arr = periods_rp1n

        log.debug(f"{self.inv_min_in_periods_rp1n_arr=} ")
        # need to do a dot product
        self.inv_min_rp1n_arr = np.einsum(
            "xn,rxn->rxn",
            demand_per_period_p1n_df.to_numpy(),
            self.inv_min_in_periods_rp1n_arr,
        )
        # https://stackoverflow.com/questions/53375161/use-numpy-array-to-replace-pandas-dataframe-values
        log.debug(f"{self.inv_min_rp1n_arr=}")
        self.supply_order()
        return self

    def supply_order(self) -> Inventory:
        """Order from supplier.

        Always order up to the safety stock
        Does not calculate economic order quantity yet
        """
        # hack here because we only do ranges for min inventory
        order_p1n_df = self.inv_min_rp1n_arr[0] - self.in_stock_p1n_df
        # negative means we have inventory above safety levels
        # so get rid of those
        # https://www.w3inventory.com/python-exercises/numpy/python-numpy-exercise-90.php
        order_p1n_df[order_p1n_df < 0] = 0
        # now gross up the order to the economic order quantity
        order_p1n_df = self.round_up_to_eoc(order_p1n_df)
        self.log.debug("supply order\n%s", order_p1n_df)
        self.fulfill(order_p1n_df)
        return self

    # https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    def round_up_to_eoc(self, order_p1n_df):
        """Round order up the economic order quantity.

        Roundup
        """
        # So take the order and then get the distance to the eoc
        # by using modulo
        # https://stackoverflow.com/questions/50767452/check-if-dataframe-has-a-zero-element
        # https://numpy.org/doc/stable/reference/generated/numpy.any.html
        # https://softwareengineering.stackexchange.com/questions/225956/python-assert-vs-if-return
        # do not use asserts they are stripped with optimization, raise errors
        if np.any(self.inv_eoc_p1n_df < 1):
            raise ValueError(
                f"EOC should never be less than 1 {self.inv_eoc_p1n_df=}"
            )

        if np.any(order_p1n_df < 0):
            raise ValueError(
                f"Orders should be never be negative {order_p1n_df=}"
            )

        return (
            order_p1n_df
            + (self.inv_eoc_p1n_df - order_p1n_df) % self.inv_eoc_p1n_df
        )

    def fulfill(self, order_p1n_df):
        """Fulfill an order form supplier.

        This is a stub in that all orders are immediatley fulfilled
        """
        self.log.debug("fulfilled immediately\n%s", order_p1n_df)
        self.in_stock_p1n_df += order_p1n_df
        self.log.debug("inventory\n%s", self.in_stock_p1n_df)

    def order(self, demand_p1n_df):
        """Order by Customer from Inventory.

        Take the demand and then return what you can
        In this simple model which you can override

        It will check what is in inventory and then call the delivery_fn method

        returns: whats available to ship
        """
        # Return as much as we can
        # the simple min won't work, need an element0-wise minimum
        # https://numpy.org/doc/stable/reference/generated/numpy.minimum.html
        deliver_p1n_df = np.minimum(demand_p1n_df, self.in_stock_p1n_df)
        self.in_stock_p1n_df -= deliver_p1n_df

        # now restock
        self.supply_order()
        return deliver_p1n_df

    def res_dataframe(self, arr: np.ndarray) -> pd.DataFrame:
        """Inventory Model.

        Dataframe setting
        """
        df = set_dataframe(
            arr,
            self.config["Label"].get(),
            index="Pop Level l",
            columns="Inventory n",
        )
        return df
