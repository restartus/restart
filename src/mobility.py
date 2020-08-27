"""Mobility Model.

Mobility modeling
"""
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore # noqa: F401
import pandas as pd  # type: ignore # noqa: F401

from base import Base
from log import Log
from data import Data


class Mobility(Base):
    """Governs how we act.

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)
        log = self.log

        self.mobility_mM_tr: Optional[Data] = None
        log.debug(f"{self.mobility_mM_tr=}")
