"""The Resource Model.

What resources are and how they are consumed
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
import logging
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from base import Base

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
        Safety stock. the minimum inventory level

    Need to be done do an economic order quantity that varies by level and item
        Economic Order Quantity. inv_eoc_ln_df
    """

    def __init__(
        self,
        model,
        attr_na_df=None,
        cost_ln_df=None,
        inv_initial_ln_df=None,
        inv_eoc_ln_df=None,
        safety_stock_ln_df=None,
    ):
        """Initialize the Resources.

        Does a read in
        """
        # to pick up the description
        super().__init__()

        # create a sublogger if a root exists in the model
        global log
        self.log = log
        if model.log_root is not None:
            log = self.log = model.log_root.log_class(self)

        """Initialize the Resource object
        This uses the Frame object and populates it with default data unless yo
        override it
        """
        self.log.debug("in %s", __name__)
        # initial inventory defaults to zero
        # need labels for later
        self.dim = model.dim
        self.label = model.label

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

        self.attr_na_arr = model.data["Resource n"]["Res Attr Data na"]
        self.attr_na_df = pd.DataFrame(
            self.attr_na_arr,
            index=self.label["Resource n"],
            columns=self.label["Res Attribute a"],
        )
        log.debug(f"{self.attr_na_df=}")

        self.set_description(
            f"{self.attr_na_df=}",
            model.description["Resource n"]["Res Detail na"]
        )

        self.cost_ln_arr = model.data["Resource n"]["Pop Level Res Cost ln"]
        self.cost_ln_df = pd.DataFrame(
                self.cost_ln_arr,
                index=self.label["Pop Level l"],
                columns=self.label["Resource n"],
            )
        log.debug(f"{self.cost_ln_df=}")
        self.set_description(
            f"{cost_ln_df=}",
            model.description["Resource n"]["Pop Level Res Cost ln"]
        )

        self.inv_initial_ln_arr = model.data["Resource n"]["Res Inventory Initial ln"]
        self.inv_initial_ln_df = pd.DataFrame(
                self.inv_initial_ln_arr,
                index=self.label["Pop Level l"],
                columns=self.label["Resource n"],
            )
        log.debug(f"{self.inv_initial_ln_df=}")
        self.set_description(
            f"{self.inv_initial_ln_df=}".split("=")[0],
            model.description["Resource n"]["Res Inventory Initial ln"]
        )
        log.debug(f"{self.description['inv_initial_ln_df']}")

        self.inventory_ln_df = self.inv_initial_ln_df
        log.debug(f"Setting initial inventory {self.inventory_ln_df=}")

        self.inv_eoc_ln_arr = model.data["Resource n"]["Res Inventory EOC ln"]
        log.debug(f"{self.inv_eoc_ln_arr=}")
        self.inv_eoc_ln_df = pd.DataFrame(
                self.inv_eoc_ln_arr,
                index=self.label["Pop Level l"],
                columns=self.label["Resource n"],
            )
        # ensure we don't have any negatives
        self.inv_eoc_ln_df[self.inv_eoc_ln_df < 1] = 1
        log.debug(f"{self.inv_eoc_ln_df=}")

        self.set_description(
            f"{self.inv_eoc_ln_df=}",
            model.description["Resource n"]["Res Inventory EOC ln"]
        )
        log.debug(f"{self.description['inv_eoc_ln_df']}")

        if safety_stock_ln_df is None:
            safety_stock_ln_df = self.inv_initial_ln_df
        self.safety_stock(safety_stock_ln_df)
        self.set_description(
            f"{self.safety_stock_ln_df=}",
            model.description["Resource n"]["Res Inventory Initial ln"]
        )

    def set_stockpile_days(self, model, days: int):
        """Set stockpile days for all resources.

        A helper function which spreads the days across all populations nad all
        columns
        """
        # new in Python 3.6
        safety_stock_days_ln_df = pd.DataFrame(
            days
            * np.ones(
                (len(self.label["Pop Level"]), len(self.label["Resource"]))
            ),
            index=self.label["Pop Level"],
            columns=self.label["Resource"],
        )
        self.log.debug(f"{safety_stock_days_ln_df=}")
        self.set_stockpile(
            model.population.level_total_demand_ln_df,
            safety_stock_days_ln_df=safety_stock_days_ln_df,
        )

    def set_stockpile(
        self,
        level_total_demand_ln_df,
        safety_stock_days_ln_df: pd.DataFrame = None,
    ):
        """Set a stock pile in days of demand.

        Stockpile set
        """
        if log is not self.log:
            raise ValueError(f"{log=} is not {self.log=}")
        if safety_stock_days_ln_df is None:
            # place holder just 30 days for essential
            safety_stock_days_ln_arr = np.array([[30, 30], [0, 0]])
            safety_stock_days_ln_df = pd.DataFrame(
                safety_stock_days_ln_arr,
                index=self.label["Pop Level"],
                columns=self.label["Resource"],
            )
            self.log.debug(
                "Safety_stock_days_ln_df\n%s", safety_stock_days_ln_df
            )

        self.log.debug(
            "Population Level Total Demand\n%s", level_total_demand_ln_df
        )
        # need to do a dot product
        new_safety_stock_ln_df = (
            level_total_demand_ln_df * safety_stock_days_ln_df.values
        )
        self.log.debug("safety stock %s", new_safety_stock_ln_df)
        self.safety_stock(new_safety_stock_ln_df)

    def safety_stock(self, safety_stock_ln_df):
        """Set or reset safety stock.

        Triggers a reorder if needed
        """
        log.debug("set safety_stock to\n%s", safety_stock_ln_df)
        self.safety_stock_ln_df = safety_stock_ln_df
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

        return order_ln_df + (self.inv_eoc_ln_df - order_ln_df) % self.inv_eoc_ln_df

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
