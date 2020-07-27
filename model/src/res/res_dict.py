"""The Resource Model.

Reads from dictionary for defaults
"""
import logging
from typing import Union

import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from modeldata import ModelData
from resourcemodel import Resource
from util import Log, set_dataframe


class ResourceDict(Resource):
    """ResourceDict - pulls resources from the default config yaml files.

    This can be a default for testing
    """

    def __init__(
        self, data: ModelData, log_root: Log = None,
    ):
        """Initialize the resources.

        Reads from the default config yaml files
        """
        # to pick up the description
        super().__init__(log_root=log_root)

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        self.log.debug(f"in {__name__}")

        # need labels for later since we do not have access to model
        self.label = data.label

        self.attr_na_arr = data.value["Resource n"]["Res Attr Data na"]
        self.attr_na_df = set_dataframe(
            self.attr_na_arr,
            data.label,
            index="Resource n",
            columns="Res Attribute a",
        )
        self.attr_na_df.index.name = "Resources n"
        self.attr_na_df.columns.name = "Res Attr a"
        log.debug(f"{self.attr_na_df=}")
        self.set_description(
            f"{self.attr_na_df=}",
            data.description["Resource n"]["Res Attr Data na"],
        )

        self.cost_ln_arr = data.value["Resource n"]["Pop Level Res Cost ln"]
        self.cost_ln_df = self.res_dataframe(np.array(self.cost_ln_arr).T)
        log.debug(f"{self.cost_ln_df=}")
        self.set_description(
            f"{self.cost_ln_df=}",
            data.description["Resource n"]["Pop Level Res Cost ln"],
        )

        self.inv_initial_ln_arr = data.value["Resource n"][
            "Res Inventory Initial ln"
        ]
        self.inv_initial_ln_df = self.res_dataframe(
            np.array(self.inv_initial_ln_arr).T
        )
        log.debug(f"{self.inv_initial_ln_df=}")
        self.set_description(
            f"{self.inv_initial_ln_df=}".split("=")[0],
            data.description["Resource n"]["Res Inventory Initial ln"],
        )
        log.debug(f"{self.description['inv_initial_ln_df']}")
        # be careful you want a copy here so inv_initial stays the same
        self.inventory_ln_df = self.inv_initial_ln_df.copy()
        log.debug(f"Setting initial inventory {self.inventory_ln_df=}")
        self.set_description(
            f"{self.inventory_ln_df=}".split("=")[0],
            data.description["Resource n"]["Res Inventory ln"],
        )

        self.inv_eoc_ln_arr = data.value["Resource n"]["Res Inventory EOC ln"]
        log.debug(f"{self.inv_eoc_ln_arr=}")
        self.inv_eoc_ln_df = self.res_dataframe(
            np.array(self.inv_eoc_ln_arr).T
        )
        # ensure we don't have any non-zero numbers
        self.inv_eoc_ln_df[self.inv_eoc_ln_df < 1] = 1
        log.debug(f"{self.inv_eoc_ln_df=}")
        self.set_description(
            f"{self.inv_eoc_ln_df=}",
            data.description["Resource n"]["Res Inventory EOC ln"],
        )
        log.debug(f"{self.description['inv_eoc_ln_df']}")

        safety_stock_ln_arr = data.value["Resource n"][
            "Res Inventory Safety Stock ln"
        ]
        self.safety_stock_ln_df = self.res_dataframe(
            np.array(safety_stock_ln_arr).T
        )
        self.set_description(
            f"{self.safety_stock_ln_df=}",
            data.description["Resource n"]["Res Inventory Safety Stock ln"],
        )

        self.average_demand_ln_arr = data.value["Resource n"][
            "Res Inventory Average Demand ln"
        ]
        self.average_demand_ln_df = self.res_dataframe(
            np.array(self.average_demand_ln_arr).T
        )
        self.set_description(
            f"{self.average_demand_ln_df=}",
            data.description["Resource n"]["Res Inventory Average Demand ln"],
        )

        self.stockpile_days_ln_arr = data.value["Resource n"][
            "Res Inventory Stockpile Days ln"
        ]
        self.stockpile_days_ln_df = self.res_dataframe(
            np.array(self.stockpile_days_ln_arr).T
        )
        self.set_description(
            f"{self.stockpile_days_ln_df=}",
            data.description["Resource n"]["Res Inventory Stockpile Days ln"],
        )

    def set_stockpile_days(self, days: Union[np.ndarray, int]) -> None:
        """Set stockpile days for all resources.

        A helper function which spreads the days across all populations nad all
        columns
        """
        # type declarations for mypy
        self.stockpile_days_ln_df: pd.DataFrame
        self.safety_stock_ln_df: pd.DataFrame

        log = self.log
        # https://numpy.org/doc/stable/reference/generated/numpy.empty_like.html
        if type(days) is int:
            self.stockpile_days_ln_arr = days * np.ones_like(
                self.inventory_ln_df
            )
        else:
            self.stockpile_days_ln_arr = days
        self.stockpile_days_ln_df[:] = self.stockpile_days_ln_arr
        log.debug(f"{self.stockpile_days_ln_df=}")

        # need to do a dot product
        self.safety_stock_ln_arr = np.array(
            self.average_demand_ln_df
        ) * np.array(self.stockpile_days_ln_df)
        # https://stackoverflow.com/questions/53375161/use-numpy-array-to-replace-pandas-dataframe-values
        self.safety_stock_ln_df[:] = self.safety_stock_ln_arr
        log.debug(f"{self.safety_stock_ln_df=}")

        self.supply_order()

    def supply_order(self):
        """Order from supplier.

        Always order up to the safety stock
        Does not calculate economic order quantity yet
        """
        order_ln_df = self.safety_stock_ln_df - self.inventory_ln_df
        # negative means we have inventory above safety levels
        # so get rid of those
        # https://www.w3resource.com/python-exercises/numpy/python-numpy-exercise-90.php
        order_ln_df[order_ln_df < 0] = 0
        # now gross up the order to the economic order quantity
        order_ln_df = self.round_up_to_eoc(order_ln_df)
        self.log.debug("supply order\n%s", order_ln_df)
        self.fulfill(order_ln_df)

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
        deliver_ln_df = min(demand_ln_df, self.inventory_ln_df)
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
