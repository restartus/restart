"""The Resource Model.

What resources are and how they are consumed
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
import logging
from typing import Optional, Union

import numpy as np  # type: ignore
import pandas as pd  # type: ignore
from base import Base
from modeldata import ModelData
from util import Log


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
            self,
            data: ModelData = None,
            log_root: Log = None,
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

        self.attr_na_df: Optional[pd.DataFrame] = None
        self.cost_ln_df: Optional[pd.DataFrame] = None
        self.inv_initial_ln_df: Optional[pd.DataFrame] = None
        self.inventory_ln_df: Optional[pd.DataFrame] = None
        self.inv_eoc_ln_df: Optional[pd.DataFrame] = None
        self.safety_stock_ln_df: Optional[pd.DataFrame] = None
        self.average_demand_ln_df: Optional[pd.DataFrame] = None
        self.stockpile_days_ln_df: Optional[pd.DataFrame] = None

    def set_stockpile_days(
            self,
            days: Union[np.ndarray, int]) -> None:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")

    def supply_order(self) -> None:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")

    def round_up_to_eoc(self,
                        order_ln_df: pd.DataFrame) -> pd.DataFrame:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")
        return order_ln_df

    def fulfill(self,
                order_ln_df: pd.DataFrame) -> None:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")

    def demand(self,
               demand_ln_df: pd.DataFrame) -> pd.DataFrame:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")
        return demand_ln_df

    def res_dataframe(self,
                      arr: np.ndarray) -> pd.DataFrame:
        """Template function.

        Does nothing
        """
        log = self.log
        log.debug("Template")
        return pd.DataFrame(arr)
