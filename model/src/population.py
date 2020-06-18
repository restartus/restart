import numpy as np
import pandas as pd


class Population:
    """ Population objects are created here
    It has a default model in it for testing which is the Bharat model
    You should override it with a new child class


    Population statistics and model for population
    Initially this containes population of p x 1
    Later it will be p x d where d are the detail columns
    For instance the number of covid patients
    The number of trips or visits or runs for a given population

    The second matrix p population describes is how to map population to
    l consumption levels to give a p x l. Long term this becomes d x p x l
    So that you can have a different run rate for each detail d of population

    """
    def __init__(self, model):

        # set the arrays of values
        self.pop_details_values = np.array([735.2, 7179.6])
        self.pop_details_df = pd.DataFrame(self.pop_details_values,
                                           index=self.pop_labels,
                                           columns=self.detail_labels)
        print('pop_levels, p x d', self.pop_details_values.shape)

        # set the population by consumption levels
        self.pop_consume_values = np.zeros([self.pop_len, self.level_len])
        self.pop_consume_values[0, -1] = self.pop_levels_values[0, -2] = 0.5
        self.pop_consume_values[1, 1] = 1.0
        # https://docs.python.org/3/library/pdb.html
        print('pop_consume, p x l', self.pop_consume_values.shape)

        self.pop_consume_df = pd.DataFrame(self.pop_levels_values,
                                           index=self.pop_labels,
                                           columns=self.level_labels)
