"""Econometric model.

The main way we integrate economic activity.
"""
# https://numpydoc.readthedocs.io/en/latest/format.html
# https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html
# note that the type ignor and noqa lines are space sensitive
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from model import Model
from typing import Optional

log = logging.getLogger(__name__)


class Economy(Base):
    """Economy - Manages the economy.

    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    # no variable here unless you want them the same across all classes
    # see https://docs.python.org/3/tutorial/classes.html

    def __init__(self, model: Model, type: Optional[str] = None):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        # create a sublogger if a root exists in the model
        global log
        self.log = log
        if model.log_root is not None:
            log = self.log = model.log_root.log_class(self)

        if type is not None:
            log.debug(f"not implemented {type=}")
