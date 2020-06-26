"""
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
import pandas as pd
import numpy as np


class Resource:
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
    """
    def __init__(self, model,
                 attribute_na_df: None,
                 cost_ln_df: None,
                 initial_inventory_ln_df: None,
                 safety_stock_ln_df: None):
        """Initialize the Resource object

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # initial inventory defaults to zero
        self.dim = {'l': model.dim['l'],
                    'n': model.dim['n']}

        # use Bharat model as default
        if attribute_na_df is None:
            attribute_na_arr = np.array([[1, 2], [2, 3]])
            attribute_na_df = pd.DataFrame(attribute_na_arr,
                                           index=model.label["Resource"],
                                           columns=model.label["Res Attribute"])
        self.attr_na_arr = attribute_na_df.values
        self.attr_na_df = attribute_na_df

        """Maps population to the essential levels for simpler analysis
        The first is a cost matrix for essential level what is their cost for
        each of n items or e x n This is essential stockpile by essential level
        so which tells you how many days of stockpile you need
        """
        if cost_ln_df is None:
            cost_ln_arr = np.array([[3, 0.5],
                                    [4.5, 0.75]])
            cost_ln_df = pd.DataFrame(cost_ln_arr,
                                      index=model.label["Level"],
                                      columns=model.label["Resource"])

        self.cost_ln_arr = cost_ln_df.values
        self.cost_ln_df = cost_ln_df

        if initial_inventory_ln_df is None:
            initial_inventory_ln_df = pd.DataFrame(np.zeros((self.dim['l'],
                                                             self.dim['n'])),
                                                   index=model.label['Level'],
                                                   columns=model.label['Resource'])
        self.inventory_ln_df = initial_inventory_ln_df

        if safety_stock_ln_df is None:
            safety_stock_ln_df = initial_inventory_ln_df
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
        self.fulfill(order_ln_df)

    def fulfill(self, order_ln_df):
        """Fulfill an order form supplier
        This is a stub in that all orders are immediatley fulfilled
        """
        print('fulfilled immediately', order_ln_df)
        self.inventory_ln_df += order_ln_df

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
