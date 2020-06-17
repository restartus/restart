
# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
from typing import List
from pandas import pd


class Resource():
    """Resource - Manages all the resources that are used in the model

 Today this is the first thing called, but later, starting anywhere works and
 the Model class adds things until they are full and then creates the
 computation graph

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
        self.frame = pd.DataFrame(
                 [[1, 2], [2, 3]],
                 index=["Units", "Dimensions"],
                 columns=["N95", "ASTM3"])
