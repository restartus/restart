"""Filter Model.

Filter the model to what's interesting. This is what Dashboard can call on when
users are done filtering.
"""

import numpy as np  # type: ignore # noqa: F401
import pandas as pd  # type: ignore # noqa: F401

from base import Base
from log import Log


# TODO: This will be much easier once we add geo to it
class Filter(Base):
    """Governs how we act.

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    """

    def __init__(
        self,
        log_root: Log = None,
        county: str = None,
        state: str = None,
        subpop: str = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)

        log = self.log

        self.location = {"county": county, "state": state}
        log.debug(f"{self.location=}")
        self.subpop = subpop
        log.debug(f"{self.subpop=}")
