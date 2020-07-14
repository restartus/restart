"""Mobility Model.

Mobility modeling
"""
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from modeldata import ModelData
from util import Log
from typing import Optional

log = logging.getLogger(__name__)


class Mobility(Base):
    """The amount of acivity and movement.

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        data: ModelData,
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
        global log
        if log_root is not None:
            self.log_root = log_root
            log = self.log = self.log_root.log_class(self)
        # the sample code to move up the logging for a period and then turn it
        # off
        self.log_root.con.setLevel(logging.DEBUG)
        log.debug(f"in {__name__=}")
        self.log_root.con.setLevel(logging.WARNING)

        if type is not None:
            log.debug(f"not implemented {type=}")
