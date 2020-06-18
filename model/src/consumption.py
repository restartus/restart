import pandas as pd
import numpy as np


class Consumption:
    """How are resources consumed by different levels in a population
    This is the key first chart in the original model.
    It takes a set of l protection levels and then for each of n resources,
    provides their burn rate. So it is a dataframe that is l x n

    In this first version, burn rates are per capita, that is per person in a
    given level.

    In a later version, we will allow different "burn rates" by population
    attributes so this becomes a 3 dimensional model. For convenience, the
    Frame object we have retains objects in their simple dataframe form since
    it is easy to extract

    For multidimenstional indices, we keep both the n-dimensional array
    (tensor) and also have a method ot convert it to a multiindex for use by
    Pandas

    There is a default mode contained here for testing, you should override
    this by creating a child class and overriding the init

    """
    def __init__(self, model):
        # note these are defaults for testing
        self.ln_values = np.array([[0, 0],
                                   [0, 1],
                                   [0, 2],
                                   [0.1, 3],
                                   [0.2, 4],
                                   [0.3, 6],
                                   [1.18, 0]])

        self.ln_df = pd.DataFrame(self.consume_resourcevalues,
                                  columns=model.label["Resource"],
                                  index=model.label["Consumption"])
