"""The Resource Model.

What resources are and how they are consumed
https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
# allows return self typing to work
from __future__ import annotations

from typing import Optional

import confuse  # type: ignore

from base import Base
from data import Data
from log import Log


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
        self,
        config: confuse.Configuration,
        log_root: Log = None,
    ):
        """Initialize the Resources.

        Does a read in
        """
        # initialize logging and description
        super().__init__(log_root=log_root)
        log = self.log
        self.config = config
        log.debug(f"in {__name__}")

        # Filling these is the job of the child classes
        self.resource_nN_ur: Optional[Data] = None
        self.res_by_popsum1_cost_per_unit_p1n_us: Optional[Data] = None
