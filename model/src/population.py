#
# Population statistics
#
import pandas as pd


def population_label():
    population_name = ['Healthcare employees',
                       'Non-employees of Heathcare companies']
    population_details = ['Population']
    return ({'name': population_name,
             'details': population_details})


def population(model):
    population_data = [735.2, 7179.6]

    population_df = pd.DataFrame(population_data,
                                 index=model.population_label['name'],
                                 columns=model.population_label['details'])
    return population_df
