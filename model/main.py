#
# Restart.us Main Module
#
# Eventually this will become a class and we will
# keep the constants like names as private class variables
#
# https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python
#

# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
# explains that you can split a class into separate files by
# putting these inside the class definition
# http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
# Before we move to full modules, just import locally
from resource import resource_name
from population import population, population_label
from consumption import usage_by_level, level_name, level_by_population

import pandas as pd


# https://www.w3schools.com/python/python_classes.asp
class Model:
    def __init__(self, resource_name, population_label, level_name):
        self.resource_name = resource_name
        # population has population rows details
        self.population_label = population_label
        self.level_name = level_name


def main():
    print('hello world')
    model = Model(resource_name(), population_label(), level_name())
    print(model, model.resource_name)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    Population_df = population(model)
    print('Population\n', Population_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    Usage_by_level_df = usage_by_level(model)
    print('Usage by level\n', Usage_by_level_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    Levels_by_population_df = level_by_population(model)
    print('Usage by population\n', Levels_by_population_df)

    # Required equipment is p poulation rows for each resource n
    # which we can get with a mac p x l * l x n
    Resource_by_population_array = Usage_by_level_df @ Levels_by_population_df
    print('Resources needed by population\n', Resource_by_population_array)
    # now convert to a dataframe

    Resource_by_population_df = pd.DataFrame(Resource_by_population_array,
                                             columns=model.resource_name,
                                             index=model.level_name)
    print('Resources needed by population df\n', Resource_by_population_df)


if __name__ == "__main__":
    main()
