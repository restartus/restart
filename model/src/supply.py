import numpy as np
import pandas as pd


class Essential():
    """Maps population to the essential levels for simpler analysis

    The first is a cost matrix for essential level what is their cost for each
    of n items or e x n 
    This is essential stockpile by essential so e x n which tells you how
    many days of stockpile you need

    """
    def __init__(self, model):
        self.cost_per_resource_en_array = np.array([[3, 0.5],
                                                   [4.5, 0.75]])

        self.cost_per_resource_en_df = pd.DataFrame(
                self.cost_per_resource_en_array,
                index=model.label["Essential"],
                columns=model.label["Resource"])

        # place holder just 30 days for essential and then zero for the rest
        self.stockpile_required_en_array = np.array([[30, 30],
                                                     [0, 0]])

        self.stockpile_required_en_df = pd.DataFrame(
                self.stockpile_required_en_array,
                index=model.label["Essential"],
                columns=model.label["Resource"])
