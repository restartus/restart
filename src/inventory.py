"""The Inventory Model.

What inventory are and how they are consumed
"""
# allows return self typing to work
from __future__ import annotations

# For slices of parameters
from enum import Enum
from typing import List

import confuse  # type: ignore
import numpy as np  # type: ignore

from base import Base
from data import Data
from log import Log


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
        self,
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
        log.debug(f"in {__name__}")

        self.inv_by_popsum1_total_rp1n_tc = Data(
            "inv_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )

        self.inv_by_popsum1_param_iIp1n_tp = Data(
            "inv_by_popsum1_param_iIp1n_tp", config, log_root=log_root
        )
        log.debug(f"{self.inv_by_popsum1_param_iIp1n_tp.df=}")

        # TODO: This should be taken from the param file
        self.inv_init_by_popsum1_total_rp1n_tc = Data(
            "inv_init_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )
        log.debug(f"set inv to {self.inv_init_by_popsum1_total_rp1n_tc=}")
        self.inv_eoq_by_popsum1_total_rp1n_tc = Data(
            "inv_eoq_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )
        self.inv_min_by_popsum1_total_rp1n_tc = Data(
            "inv_min_by_popsum1_total_rp1n_tc", config, log_root=log_root
        )

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

        # can only set minmum once inv_min exists and order too
        self.set_min(self.inv_init_by_popsum1_total_rp1n_tc)

    def set_average_orders_per_period(
        self, inv_average_orders_by_popsum1_per_period_rp1n_uf: Data
    ):
        """Set Average Inventory Used Every Period.

        This could just be a simple set but leave here for clarity
        """
        self.inv_average_orders_by_popsum1_per_period_rp1n_uf = (
            inv_average_orders_by_popsum1_per_period_rp1n_uf
        )

    def set_min_in_periods(
        self,
        min_periods_r_pc: List,
    ) -> Inventory:
        """Sets the Minimum Inventory as measured in Average Days Shipments.

        A Helper function that fill out an entire array and then passes it
        down
        """
        log = self.log
        log.debug(f"{min_periods_r_pc=}")
        self.inv_min_by_popsum1_in_periods_rp1n_pc.array = np.einsum(
            "r,rxn->rxn",
            min_periods_r_pc,
            np.ones_like(self.inv_min_by_popsum1_in_periods_rp1n_pc.array),
        )
        self.set_min_in_periods_array(
            self.inv_min_by_popsum1_in_periods_rp1n_pc
        )
        return self

    def set_min_in_periods_array(
        self,
        min_periods_rp1n_tc: Data,
    ) -> Inventory:
        """Set with an array that is for all resources in periods."""
        log = self.log
        self.inv_min_by_popsum1_in_periods_rp1n_pc.array = (
            min_periods_rp1n_tc.array
        )
        log.debug(f"{self.inv_min_by_popsum1_in_periods_rp1n_pc.df=} ")

        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        # note we need r=1 for this to work so we insert an empty dimension
        # https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html
        # needed this before we started calling with full range
        # self.inv_min_by_popsum1_per_period_rp1n_uc.array = np.expand_dims(
        #     self.inv_min_by_popsum1_per_period_rp1n_uc.array, axis=0
        # )
        # need to do a dot product
        self.inv_min_by_popsum1_total_rp1n_tc.array = np.einsum(
            "rxn,rxn->rxn",
            min_periods_rp1n_tc.array,
            self.inv_average_orders_by_popsum1_per_period_rp1n_uf.array,
        )
        self.set_min(self.inv_min_by_popsum1_total_rp1n_tc)
        return self

    def set_min(self, min_by_popsum1_total_rp1n_tc: Data) -> Inventory:
        """Set the minimum inventory in periods_r.

        This sets the minimum inventory and then forces an order in case we are
        below the minimum
        """
        log = self.log

        # https://stackoverflow.com/questions/53375161/use-numpy-array-to-replace-pandas-dataframe-values
        self.inv_by_popsum1_total_rp1n_tc.array = (
            min_by_popsum1_total_rp1n_tc.array
        )
        log.debug(f"{self.inv_by_popsum1_total_rp1n_tc.df=}")
        self.supply_order()
        return self

    def supply_order(self) -> Inventory:
        """Order from supplier.

        Order up to the minimum inventory
        """
        # hack here because we only do ranges for min inventory
        self.inv_order_by_popsum1_total_rp1n_tc.array = (
            self.inv_min_by_popsum1_total_rp1n_tc.array
            - self.inv_by_popsum1_total_rp1n_tc.array
        )
        # negative means we have inventory above safety levels
        # so get rid of those
        # https://www.w3inventory.com/python-exercises/numpy/python-numpy-exercise-90.php
        self.inv_order_by_popsum1_total_rp1n_tc.array[
            self.inv_order_by_popsum1_total_rp1n_tc.array < 0
        ] = 0
        # now gross up the order to the economic order quantity
        self.round_up_to_eoq(self.inv_order_by_popsum1_total_rp1n_tc)
        self.log.debug(f"{self.inv_order_by_popsum1_total_rp1n_tc.df=}")

        # now that we have an order rounded up and ready, let's get supply
        self.fulfill(self.inv_order_by_popsum1_total_rp1n_tc)
        return self

    # https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    def round_up_to_eoq(self, order_by_popsum1_total_rp1n_tc: Data) -> Data:
        """Round order up the economic order quantity.

        Each order needs to get rounded up to an economic quantity
        """
        if np.any(self.inv_eoq_by_popsum1_total_rp1n_tc.array <= 0):
            raise ValueError(
                f"EOQ not positive {self.inv_eoq_by_popsum1_total_rp1n_tc.df=}"
            )

        if np.any(order_by_popsum1_total_rp1n_tc.array < 0):
            raise ValueError(
                f"Negative order in {order_by_popsum1_total_rp1n_tc.df=}"
            )

        # So take the order and then get the distance to the eoc
        # by using modulo
        # https://stackoverflow.com/questions/50767452/check-if-dataframe-has-a-zero-element
        # https://numpy.org/doc/stable/reference/generated/numpy.any.html
        # https://softwareengineering.stackexchange.com/questions/225956/python-assert-vs-if-return
        # do not use asserts they are stripped with optimization, raise errors
        return (
            order_by_popsum1_total_rp1n_tc.array
            + (
                self.inv_eoq_by_popsum1_total_rp1n_tc.array
                - order_by_popsum1_total_rp1n_tc.array
            )
            % self.inv_eoq_by_popsum1_total_rp1n_tc.array
        )

    def fulfill(self, order_by_popsum1_total_rp1n_tc: Data):
        """Fulfill an order form supplier.

        This is a stub in that all orders are immediatley fulfilled
        """
        log = self.log
        log.debug(f"fulfill {order_by_popsum1_total_rp1n_tc=}")
        self.inv_by_popsum1_total_rp1n_tc.array += (
            order_by_popsum1_total_rp1n_tc.array
        )
        log.debug(f"{self.inv_by_popsum1_total_rp1n_tc.df=}")

    def order(self, order_by_popsum1_total_rp1n_tc: Data) -> Data:
        """Order by Customer from Inventory.

        Take a new order and then return what you can

        It will check what is in inventory and then call the delivery method
        returns: whats available to ship
        """
        # Return as much as we can so if the order is bigger than
        # the inventory, just ship it all out.
        # the simple min won't work, need an element0-wise minimum
        # https://numpy.org/doc/stable/reference/generated/numpy.minimum.html
        self.inv_order_by_popsum1_total_rp1n_tc.array = np.minimum(
            order_by_popsum1_total_rp1n_tc.array,
            self.inv_by_popsum1_total_rp1n_tc.array,
        )

        # ship it!
        self.inv_by_popsum1_total_rp1n_tc.array -= (
            self.inv_order_by_popsum1_total_rp1n_tc.array
        )

        # now restock
        self.supply_order()
        return self.inv_order_by_popsum1_total_rp1n_tc
