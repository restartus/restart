#
# Resource usage by protection level returned
#
import pandas as pd
import numpy as np


def level_name():
    level_name = ['WA0', 'WA1', 'WA2', 'WA3', 'WA4', 'WA5', 'WA6']
    return level_name


def level_by_population(model):
    level_by_population_array = np.zeros([len(model.population_label),
                                          len(model.level_name)])

    level_by_population_array[0, 5:6] = 0.5
    level_by_population_array[1, 1] - 1.0
    return level_by_population


# This is rows that are levels adn then usage of each resource  or l, n
# When population become n x d, then there will be a usage
# level for each do, so this become d x p x n
def usage_by_level(model):
    usage_by_level_array = [[0, 0],
                            [0, 1],
                            [0, 2],
                            [0.1, 3],
                            [0.2, 4],
                            [0.3, 6],
                            [1.18, 0]]
    usage_by_level_df = pd.DataFrame(usage_by_level_array,
                                     columns=model.resource_name,
                                     index=model.level_name)
    return usage_by_level_df
