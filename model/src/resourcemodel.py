"""The Resource Model.

What resources are and how they are consumed
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
import logging
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from base import Base
from modeldata import ModelData
from util import Log, set_dataframe
from typing import Union

log = logging.getLogger(__name__)


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
        Safety stock. the minimum inventory level in days
        Average Demand. This is used for min stockpilg

    Need to be done do an economic order quantity that varies by level and item
        Economic Order Quantity. inv_eoc_ln_df
    """

    # no variables here unless you want class variables the same across all
    # instances

    def __init__(
        self, data: ModelData, log_root: Log = None, type: str = None,
    ):
        """Initialize the Resources.

        Does a read in
        """
        # to pick up the description
        super().__init__()

        # create a sublogger if a root exists in the model
        global log
        self.log = log
        if log_root is not None:
            self.log_root = log_root
            log = self.log = self.log_root.log_class(self)

        """Initialize the Resource object
        This uses the Frame object and populates it with default data unless yo
        override it
        """
        self.log.debug("in %s", __name__)
        # initial inventory defaults to zero
        # need labels for later since we do not have access to model
        self.label = data.label

        if type is not None:
            # ignoring the type for now but will eventually link
            log.debug(f"{type=}")

        # original self initialization code
        # if attr_na_df is None:
        #     attr_na_arr = np.array([[1, 2], [2, 3]])
        #     attr_na_df = pd.DataFrame(
        #         attr_na_arr,
        #         index=self.label["Resource n"],
        #         columns=self.label["Res Attribute a"],
        #     )
        # self.attr_na_arr = attr_na_df.values
        # self.attr_na_df = attr_na_df

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
        self.cost_ln_df = self.res_dataframe(self.cost_ln_arr)
        log.debug(f"{self.cost_ln_df=}")
        self.set_description(
            f"{self.cost_ln_df=}",
            data.description["Resource n"]["Pop Level Res Cost ln"],
        )

        self.inv_initial_ln_arr = data.value["Resource n"][
            "Res Inventory Initial ln"
        ]
        self.inv_initial_ln_df = self.res_dataframe(self.inv_initial_ln_arr,)
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
        self.inv_eoc_ln_df = self.res_dataframe(self.inv_eoc_ln_arr,)
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
        self.safety_stock_ln_df = self.res_dataframe(safety_stock_ln_arr,)
        self.set_description(
            f"{self.safety_stock_ln_df=}",
            data.description["Resource n"]["Res Inventory Safety Stock ln"],
        )

        self.average_demand_ln_arr = data.value["Resource n"][
            "Res Inventory Average Demand ln"
        ]
        self.average_demand_ln_df = self.res_dataframe(
            self.average_demand_ln_arr
        )
        self.set_description(
            f"{self.average_demand_ln_df=}",
            data.description["Resource n"]["Res Inventory Average Demand ln"],
        )

        self.stockpile_days_ln_arr = data.value["Resource n"][
            "Res Inventory Stockpile Days ln"
        ]
        self.stockpile_days_ln_df = self.res_dataframe(
            self.stockpile_days_ln_arr
        )
        self.set_description(
            f"{self.stockpile_days_ln_df=}",
            data.description["Resource n"]["Res Inventory Stockpile Days ln"],
        )

    def set_stockpile_days(self, days: Union[np.ndarray, int]):
        """Set stockpile days for all resources.

        A helper function which spreads the days across all populations nad all
        columns
        """
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
        self.safety_stock_ln_arr = (
            self.average_demand_ln_arr * self.stockpile_days_ln_arr
        )
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
