""" https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
"""
# https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html
# note that the type ignor and noqa lines are space sensitive
import logging  # noqa: F401
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from model import Model
from util import setLogger

log = setLogger(__name__)


class Economy(Base):
    """Economy - Manages the economy
    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(self, model: Model):
        """Initialize the Economy object

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()
