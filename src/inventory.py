"""The Inventory Model.

What inventory are and how they are consumed
"""
# allows return self typing to work
from __future__ import annotations

# For slices of parameters
from enum import Enum
from typing import Union, List

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from base import Base
from data import Data
from log import Log
from util import set_dataframe


# https://docs.python.org/3/library/enum.html
# These are the slices used
class InvParam(Enum):
    """List positions in Inventory Parameter List."""

    INIT = 0
    EOQ = 1
    MIN = 2


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

        self.inv_by_popsum1_parameters_iIp1n_tp = Data(
            "inv_by_popsum1_parameters_iIp1n_tp", config, log_root=log_root
        )
        log.debug(f"{self.inv_by_popsum1_parameters_iIp1n_tp=}")

        self.inv_by_popsum1_total_rp1n_tc = Data(
            "inv_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )

        # a helper function
        self.inv_min_by_popsum1_per_period_rp1n_uc = Data(
            "inv_min_by_popsum1_per_period_rp1n_uc", config, log_root=log_root
        )

    def set_min_by_list(self,
                        min_period_rt_pc: List,
                        min_demand_per_period_rp1n_df: pd.Dataframe,
                        ) -> Inventory:
        log = self.log
        log.debug(f"{min_period_rt_pc=}")
        self.set_min_by_period(
            min_period_rt_pc,
            * np.ones_like(min_demand_per_period_rp1n_df)
        )

        return self

    def set_min_by_period(self,
                          min_periods_rp1n_df: pd.Dataframe,) -> Inventory:
        self.inv_min_by_popsum1_per_period_rp1n_uc.df = min_periods_rp1n_df

        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        # note we need r=1 for this to work so we insert an empty dimension
        # https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html
        self.inv_min_by_popsum1_per_period_rp1n_uc.array = np.expand_dims(
            self.inv_min_by_popsum1_per_period_rp1n_uc.array, axis=0
        )
        log.debug(f"{self.inv_min_by_popsum1_per_period_rp1n_uc=} ")
        # need to do a dot product
        set_min(np.einsum(
            "rxn,rxn->rxn",
            min_demand_per_period_rp1n_df.to_numpy(),
            self.inv_min_by_popsum1_per_period_rp1n_uc.array,
        ))
        return self

    def set_min(
        self,
        min_demand_total_rp1n_df: pd.Dataframe,
    ) -> Inventory:
        """Set the minimum inventory in periods_r.

        A helper function that sets the minimum inventory
        Based on how many periods_r (days) you want stored

        This handles ranges so you can do [30, 60, 90]
        all at once but this is not handled anywhere else
        """
        log = self.log

        # https://stackoverflow.com/questions/53375161/use-numpy-array-to-replace-pandas-dataframe-values
        log.debug(f"{self.inv_min_rp1n_arr=}")
        self.inv_min_rp1n_tc.array = np.einsum(
        self.supply_order()
        return self

    def supply_order(self) -> Inventory:
        """Order from supplier.

        Always order up to the safety stock
        Does not calculate economic order quantity yet
        """
        # hack here because we only do ranges for min inventory
        order_p1n_df = (
            self.inv_min_rp1n_arr[0] - self.inv_by_popsum1_total_rp1n_tc.array
        )
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
        log = self.log
        log.debug("fulfilled immediately\n%s", order_p1n_df)
        self.inv_by_popsum1_total_rp1n_tc.array += order_p1n_df.to_numpy()
        log.debug(f"{self.inv_by_popsum1_total_rp1n_tc.df=}")

    def order(self, order_by_popsum1_total_rp1n_tc_df):
        """Order by Customer from Inventory.

        Take a new order and then return what you can

        It will check what is in inventory and then call the delivery method
        returns: whats available to ship
        """
        # Return as much as we can
        # the simple min won't work, need an element0-wise minimum
        # https://numpy.org/doc/stable/reference/generated/numpy.minimum.html
        order_by_popsum1_total_rp1n_tc_df = np.minimum(
                                order_by_popsum1_total_rp1n_tc_df,
                                self.inv_by_popsum1_parameters_iIp1n_tp.df)
        self.inv_by_popsum1_total_rp1n_tc.array -= order_by_popsum1_total_rp1n_tc_df.to_numpy()

        # now restock
        self.supply_order()
        return order_by_popsum1_total_rp1n_tc_df

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
