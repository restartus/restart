"""Filter Model.

Filter the model to what's interesting. This is what Dashboard can call on when
users are done filtering.
"""
import logging

import numpy as np  # type: ignore # noqa: F401
import pandas as pd  # type: ignore # noqa: F401

from base import Base
from util import Log


class Filter(Base):
    """Governs how we act.

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        log_root: Log = None,
        county: str = None,
        state: str = None,
        population: str = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
            # demo code
            log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
        self.log = log

        self.location = {"county": county, "state": state}
        log.debug(f"{self.location=}")
        self.population = population
        log.debug(f"{self.population=}")
