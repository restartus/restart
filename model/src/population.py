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
        self.detail_pd_array = np.array([735.2, 7179.6])
        self.detail_pd_df = pd.DataFrame(self.detail_pd_array,
                                         index=model.label['Population'],
                                         columns=model.label['Details'])
        print('pop_levels, p x d', self.detail_pd_array.shape)

        # set the population by consumption levels
        self.consumption_pl_array = np.zeros((len(model.label['Population']),
                                              len(model.label['Consumption'])))
        self.consumption_pl_array[0, -1] = 0.5
        self.consumption_pl_array[0, -2] = 0.5
        self.consumption_pl_array[1, 1] = 1.0
        # https://docs.python.org/3/library/pdb.html
        print('population.consumption_pl_array, p x l',
              self.consumption_pl_array.shape)

        self.consumption_pl_df = pd.DataFrame(self.consumption_pl_array,
                                              index=model.label['Population'],
                                              columns=model.label['Consumption'])
