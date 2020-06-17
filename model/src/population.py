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

    """
    def __init__(self, model):

        print('set labels')
        self.pop_details_values = [735.2, 7179.6]
        # Hack to set it right
        self.pop_levels_values = np.zeros([self.pop_len, self.level_len])
        self.pop_levels_values[0, -1] = self.pop_levels_values[0, -2] = 0.5
        self.pop_levels_values[1, 1] = 1.0
        # https://docs.python.org/3/library/pdb.html
        print('each population, which levels: ', self.pop_len, self.detail_len)
        print('pop_levels, p x l', self.pop_details_values.shape)
        self.pop_levels_df = pd.DataFrame(self.pop_levels_values,
                                          index=self.pop_labels,
                                          columns=self.level_labels)
        self.pop_details_df = pd.DataFrame(self.pop_details_values,
                                           index=self.pop_labels,
                                           columns=self.detail_labels)
        self.pop_labels = ["Healthcare workers",
                           "Non-heathcare employees"],
        self.detail_labels = ["People"]
        self.level_labels = ['WA0', 'WA1', 'WA2', 'WA3', 'WA4', 'WA5', 'WA6']

        # Is this really allowed, it is doing in place edits into model
        # could also have it return a new model which is cleaner
        print('now set model with new labels')
        model.pop_labels = self.pop_labels
        model.detail_labels = self.detail_labels
        model.level_labels = self.level_labels
        model.pop_len = len(self.pop_labels)
        model.detail_len = len(self.detail_labels)
        model.level_len = len(self.level_labels)
        model.population = self

        print('set default values')
        self.pop_details_values = [735.2, 7179.6]
        # Hack to set it right
        self.pop_levels_values = np.zeros([self.pop_len, self.level_len])
        self.pop_levels_values[0, -1] = self.pop_levels_values[0, -2] = 0.5
        self.pop_levels_values[1, 1] = 1.0
        # https://docs.python.org/3/library/pdb.html
        print('each population, which levels: ', self.pop_len, self.detail_len)
        print('pop_levels, p x l', self.pop_details_values.shape)
        self.pop_levels_df = pd.DataFrame(self.pop_levels_values,
                                          index=self.pop_labels,
                                          columns=self.level_labels)
        self.pop_details_df = pd.DataFrame(self.pop_details_values,
                                           index=self.pop_labels,
                                           columns=self.detail_labels)
