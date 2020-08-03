"""The Resource Model.

What resources are and how they are consumed
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
# allows return self typing to work
from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Union

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from base import Base
from modeldata import ModelData
from util import Log, set_dataframe


class Resource(Base):
    """Resource - Manages all the resources that are used in the model.

    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation

    Stores all in lxn levels and items:
        Resource. Attributes of each
        Costs. Of the resource
        Inventory. The current inventory level
        Safety stock. the minimum inventory level in days since we have a surge
        model this is simply right now the daily rate the model shows
        Economic Order Quantity. inv_eoc_ln_df
    """

    # no variables here unless you want class variables the same across all
    # instances

    def __init__(
        self, data: ModelData = None, log_root: Log = None,
    ):
        """Initialize the Resources.

        Does a read in
        """
        # initialize logging and description
        super().__init__(log_root=log_root)
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log

        # Filling these is the job of the child classes
        self.attr_na_df: Optional[pd.DataFrame] = None
        self.cost_ln_df: Optional[pd.DataFrame] = None
        self.inv_initial_ln_df: Optional[pd.DataFrame] = None
        self.inventory_ln_df: Optional[pd.DataFrame] = None
        self.inv_eoc_ln_df: Optional[pd.DataFrame] = None
        self.average_demand_ln_df: Optional[pd.DataFrame] = None
        self.inv_min_rln_df: Optional[pd.DataFrame] = None
        self.label: Optional[Dict[Any, Any]] = None

    def set_inv_min(
        self,
        demand_per_period_ln_df: pd.DataFrame,
        periods_rln: Union[np.ndarray, int],
    ) -> Resource:
        """Set the minimum inventory in periods_r.

        A helper function that sets the minimum inventory
        Based on how many periods_r (days) you want stored
        TODO: Right now it is just using the actually demand since this is
        surge model but it should use some sort of average or statistical
        calculation
        """
        log = self.log
        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        if type(periods_rln) is int:
            log.debug(f"{periods_rln=} scalar inventory")
            # note we need r=1 for this to work so we insert an empty dimension
            # https://numpy.org/doc/stable/reference/generated/numpy.expand_dims.html
            self.inv_min_in_periods_rln_arr: np.ndarray = (
                periods_rln * np.ones_like(demand_per_period_ln_df)
            )
            self.inv_min_in_periods_rln_arr = np.expand_dims(
                self.inv_min_in_periods_rln_arr, axis=0
            )
        else:
            self.inv_min_in_periods_rln_arr = periods_rln

        log.debug(f"{self.inv_min_in_periods_rln_arr=} ")
        # need to do a dot product
        self.inv_min_rln_arr = np.einsum(
            "ln,rln->rln",
            demand_per_period_ln_df.to_numpy(),
            self.inv_min_in_periods_rln_arr,
        )
        # https://stackoverflow.com/questions/53375161/use-numpy-array-to-replace-pandas-dataframe-values
        log.debug(f"{self.inv_min_rln_arr=}")
        self.supply_order()
        return self

    def supply_order(self) -> Resource:
        """Order from supplier.

        Always order up to the safety stock
        Does not calculate economic order quantity yet
        """
        # hack here because we only do ranges for min inventory
        order_ln_df = self.inv_min_rln_arr[0] - self.inventory_ln_df
        # negative means we have inventory above safety levels
        # so get rid of those
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-90.php
        order_ln_df[order_ln_df < 0] = 0
        # now gross up the order to the economic order quantity
        order_ln_df = self.round_up_to_eoc(order_ln_df)
        self.log.debug("supply order\n%s", order_ln_df)
        self.fulfill(order_ln_df)
        return self

    # https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    def round_up_to_eoc(self, order_ln_df):
        """Round order up the economic order quantity.

        Roundup
        """
        # So take the order and then get the distance to the eoc
        # by using modulo
        # https://stackoverflow.com/questions/50767452/check-if-dataframe-has-a-zero-element
        # https://numpy.org/doc/stable/reference/generated/numpy.any.html
        # https://softwareengineering.stackexchange.com/questions/225956/python-assert-vs-if-return
        # do not use asserts they are stripped with optimization, raise errors
        if np.any(self.inv_eoc_ln_df < 1):
            raise ValueError(
                f"EOC should never be less than 1 {self.inv_eoc_ln_df=}"
            )

        if np.any(order_ln_df < 0):
            raise ValueError(
                f"Orders should be never be negative {order_ln_df=}"
            )

        return (
            order_ln_df
            + (self.inv_eoc_ln_df - order_ln_df) % self.inv_eoc_ln_df
        )

    def fulfill(self, order_ln_df):
        """Fulfill an order form supplier.

        This is a stub in that all orders are immediatley fulfilled
        """
        self.log.debug("fulfilled immediately\n%s", order_ln_df)
        self.inventory_ln_df += order_ln_df
        self.log.debug("inventory\n%s", self.inventory_ln_df)

    def demand(self, demand_ln_df):
        """Demand for resources.

        Take the demand and then return what you can
        In this simple model which you can override

        It will check what is in inventory and then call the delivery_fn method

        returns: whats available to ship
        """
        # Return as much as we can
        # the simple min won't work, need an element0-wise minimum
        # https://numpy.org/doc/stable/reference/generated/numpy.minimum.html
        deliver_ln_df = np.minimum(demand_ln_df, self.inventory_ln_df)
        self.inventory_ln_df -= deliver_ln_df

        # now restock
        self.supply_order()
        return deliver_ln_df

    def res_dataframe(self, arr: np.ndarray) -> pd.DataFrame:
        """Resource Model.

        Dataframe setting
        """
        df = set_dataframe(
            arr, self.label, index="Pop Level l", columns="Resource n"
        )
        return df
