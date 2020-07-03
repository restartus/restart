"""
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
import logging
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from base import Base
from util import setLogger

log = setLogger(__name__)
log.setLevel(logging.WARNING)


class Resource(Base):
    """Resource - Manages all the resources that are used in the model
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
        Economic Order Quantity. eoc_ln_df
    """

    def __init__(
        self,
        model,
        attr_na_df=None,
        cost_ln_df=None,
        initial_inventory_ln_df=None,
        eoc_ln_df=None,
        safety_stock_ln_df=None,
    ):
        # to pick up the description
        super().__init__()

        """Initialize the Resource object
        This uses the Frame object and populates it with default data unless yo
        override it
        """
        log.debug("in %s", __name__)
        # initial inventory defaults to zero
        # need labels for later
        self.dim = model.dim
        self.label = model.label

        # use Bharat model as default
        if attr_na_df is None:
            attr_na_arr = np.array([[1, 2], [2, 3]])
            attr_na_df = pd.DataFrame(
                attr_na_arr,
                index=self.label["Resource"],
                columns=self.label["Res Attribute"],
            )
        self.attr_na_arr = attr_na_df.values
        self.attr_na_df = attr_na_df
        log.debug(f"{self.attr_na_df=}")
        self.setDescription(
            model,
            f"{self.attr_na_df=}".split("=")[0],
            """
        ## Resource Attributes
        For all n Resources, these are the a Attributes
        of each resource.
        """,
        )

        if cost_ln_df is None:
            cost_ln_arr = np.array([[3, 0.5], [4.5, 0.75]])
            cost_ln_df = pd.DataFrame(
                cost_ln_arr,
                index=self.label["Pop Level"],
                columns=self.label["Resource"],
            )
        self.cost_ln_arr = cost_ln_df.values
        self.cost_ln_df = cost_ln_df
        log.debug("self.cost_ln_df\n%s", self.cost_ln_df)
        self.setDescription(
            model,
            f"{cost_ln_df=}".split("=")[0],
            """
        ## For Each Summary Level, the cost of Resoures
        For each of l summary levels, get the per capita cost for each of n
        Resources.
        """,
        )

        if initial_inventory_ln_df is None:
            initial_inventory_ln_df = pd.DataFrame(
                np.zeros((self.dim["l"], self.dim["n"])),
                index=self.label["Pop Level"],
                columns=self.label["Resource"],
            )
        self.inventory_ln_df = initial_inventory_ln_df
        log.debug("self.inventory_ln_df\n%s", self.inventory_ln_df)
        self.setDescription(
            model,
            f"{self.inventory_ln_df=}".split("=")[0],
            """
        ## Inventory by Population Summary Levels
        For each summarized population level l, this gives for every resource n
        the current inventory of each.
        """,
        )

        if eoc_ln_df is None:
            # default eoc is 2
            eoc_ln_arr = np.ones((self.dim["l"], self.dim["n"])) * 2
            log.debug("eoc_ln_arr\n%s", eoc_ln_arr)
            eoc_ln_df = pd.DataFrame(
                eoc_ln_arr,
                index=self.label["Pop Level"],
                columns=self.label["Resource"],
            )
        self.eoc_ln_df = eoc_ln_df
        log.debug("self.eoc_ln_df\n%s", self.eoc_ln_df)
        self.setDescription(
            model,
            f"{self.eoc_ln_df=}".split("=")[0],
            """## Economic Order Quantity
        For each summarized population level l, this gives for every resource n
        the economic order quantity for reordering.
        """,
        )

        if safety_stock_ln_df is None:
            safety_stock_ln_df = initial_inventory_ln_df
        self.safety_stock(safety_stock_ln_df)
        self.setDescription(
            model,
            f"{self.safety_stock_ln_df=}".split("=")[0],
            """## Safety Stock
        For each summarized population level l, this gives for every resource n
        the economic order quantity for reordering.
        """,
        )

    def stockpile(self, level_total_demand_ln_df, safety_stock_days_df=None):
        """Set a stock pile in days of demand
        """
        if safety_stock_days_df is None:
            # place holder just 30 days for essential
            safety_stock_days_ln_arr = np.array([[30, 30], [0, 0]])
            safety_stock_days_ln_df = pd.DataFrame(
                safety_stock_days_ln_arr,
                index=self.label["Pop Level"],
                columns=self.label["Resource"],
            )
            log.debug("Safety_stock_days_ln_df\n%s", safety_stock_days_ln_df)

        log.debug(
            "Population Level Total Demand\n%s", level_total_demand_ln_df
        )
        # need to do a dot product
        new_safety_stock_ln_df = (
            level_total_demand_ln_df * safety_stock_days_ln_df.values
        )
        log.debug("safety stock %s", new_safety_stock_ln_df)
        self.safety_stock(new_safety_stock_ln_df)

    def safety_stock(self, safety_stock_ln_df):
        """set or reset safety stock
        Triggers a reorder if needed
        """
        log.debug("set safety_stock to\n%s", safety_stock_ln_df)
        self.safety_stock_ln_df = safety_stock_ln_df
        self.supply_order()

    def supply_order(self):
        """Order from supplier
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
        log.debug("supply order\n%s", order_ln_df)
        self.fulfill(order_ln_df)

    # https://stackoverflow.com/questions/2272149/round-to-5-or-other-number-in-python
    def round_up_to_eoc(self, order_ln_df):
        """Round order up the economic order quantity
        """
        # So take the order and then get the distance to the eoc
        # by using modulo
        return order_ln_df + (self.eoc_ln_df - order_ln_df) % self.eoc_ln_df

    def fulfill(self, order_ln_df):
        """Fulfill an order form supplier
        This is a stub in that all orders are immediatley fulfilled
        """
        log.debug("fulfilled immediately\n%s", order_ln_df)
        self.inventory_ln_df += order_ln_df
        log.debug("inventory\n%s", self.inventory_ln_df)

    def demand(self, demand_ln_df):
        """Demand for resources
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
