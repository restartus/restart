# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
import pandas as pd
import numpy as np


class Resource():
    """Resource - Manages all the resources that are used in the model
    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """
    def init(self, model):
        """Initialize the Resource object

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        self.ra_array = np.array([[1, 2], [2, 3]])
        self.ra_df = pd.DataFrame(
                 index=model.label["Resource"],
                 columns=model.label["Attribute"])
