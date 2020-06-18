#
# Essential math
# determine how to compress population into meaningful categories
#
import numpy as np
import pandas as pd


def essential_name():
    essential_name = ["Essential", "Non-essential"]
    return essential_name


def population_by_essentiality(model):
    # Make it simple, just map healthcare to essential
    population_by_essentiality_array = np.eye(2)

    population_by_essentiality_df = pd.DataFrame(
            population_by_essentiality_array,
            index=model.essential_name,
            columns=model.population_label['name'])

    return population_by_essentiality_df
