# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
import pandas as pd
import numpy as np


class Economy:
    """Economy - Manages the economy
    This creates for all r resources, the list of attributes a

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
