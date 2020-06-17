#
# These are the classes that set the protection levels and manage them
# It takes in the population
#
# This actually contains two matrix
#
# For each level, what is the usage
#
import pandas as pd


class Consumption:
    """initialize consumption
    When population become n x d, then there will be a usage
    evel for each do, so this become d x p x n
    This is for each level l, what is the usage of n resources
    """
    def __init__(self, model):
        self.level_consume_values = [[0, 0],
                                     [0, 1],
                                     [0, 2],
                                     [0.1, 3],
                                     [0.2, 4],
                                     [0.3, 6],
                                     [1.18, 0]]
        self.level_consume = pd.DataFrame(self.level_consume_values,
                                          columns=model.resource_labels,
                                          index=model.level_labels)
