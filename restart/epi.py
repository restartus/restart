"""Epi model.

The disease model work.
"""

# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
# note the noqa: and type: are space sensitive
# https://stackoverflow.com/questions/51179109/set-pyflake-and-mypy-ignore-same-line
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore # noqa: F401
import pandas as pd  # type: ignore # noqa: F401

from base import Base
from data import Data
from log import Log


class Epi(Base):
    """Resource - Manages all the resources that are used in the model.

    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    # no variable here unless you want them the same across all classes
    # see https://docs.python.org/3/tutorial/classes.html
    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Epi object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)
        log = self.log

        self.epi_eE_pr: Optional[Data] = None
        log.debug(f"{self.epi_eE_pr=}")
