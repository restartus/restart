""" Behavioral
"""
import logging
import pandas as pd
import numpy as np
from base import Base

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)


class Behavioral(Base):
    """Governs how we act

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """
    def __init__(self, model):
        """Initialize the Economy object

        This uses the Frame object and populates it with default data unless yo
        override it
        """
