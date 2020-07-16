"""Consumption Model.

Consumption modeling
"""
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from modeldata import ModelData
from util import Log
from typing import Optional
from population import Population
from resourcemodel import Resource


class Consumption(Base):
    """Calculate consumption based on Population and Resource.

    Take in Pop and and Res and into model.data["Pop Res Demand pn"]
    Some parameters are to use:
    - Washington estimate
    - Mitre burn rates
    - Johns Hopkins burn rates
    - CDPH estimates
    - Ensemble

    If pop and res aren't set by default take the existing Population and
    resource already in the model.data

    With dimensions ["Population p"]["Resource n"]

    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        data: ModelData,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
            # the sample code to move up the logging for a period
            log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
        self.log = log

        if pop is None:
            log.warning("Not implemented, if no pop passed, use model.data")
        if res is None:
            log.warning("Not implemented, if no res passed, use model.data")
        if type == "Mitre":
            log.debug("Use Mitre consumption")
        elif type == "Johns Hopkins":
            log.debug("Use JHU burn rate model")
        else:
            log.debug("For anything else use Washington data")
