"""
 Restart.us Main Module

 Eventually this will become a class and we will
 keep the constants like names as private class variables

 https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python

"""

# https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
import logging

# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
# explains that you can split a class into separate files by
# putting these inside the class definition
# http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
# Before we move to full modules, just import locally
from resource import Resource
from model import Model
from population import Population
from economy import Economy
from disease import Disease

# This is the only way to get it to work needs to be in main
# https://www.programcreek.com/python/example/192/logging.Formatter
logging.basicConfig(format='{filename}:{lineno} {message}', style='{')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

# https://www.programcreek.com/python/example/192/logging.Formatter
# How we need to format
FORMATTER = logging.Formatter('{filename}:{lineno} {message}', style='{')
CH = logging.StreamHandler()
CH.setLevel(level=logging.DEBUG)
CH.setFormatter(FORMATTER)
LOG.addHandler(CH)


# https://docs.python.org/3/howto/logging-cookbook.html
LOG.info('hello world')


def main():
    """ Bootstrap the whole model creating all objects
    Bootstrap where each modules successively knows more about the world
    Population defines Pop_details[p,d], Pop_levels[p,l]

    In this version, there is a specific order of creation and implicit
    dependencies so use in this order. The notation we uses suffixes each with
    a unique letter that gives the number of elements so n x a means n resource
    by a attributes. And yes this will not work when we have more than 26
    types of dimensions :-)

    In a future revision, you can do this in any order and it will work
    - model itself
    - resource which creates the n resources (eg N95, test kit, etc.) with
      the columns being x attributes like the units and space R[n, x].
    - consumption to create burn rates for each "level" of the model. Instead
    of calculating unique burn rates per population element, we bucketize with
      the consumption level l so it returns C[l, n]

    And if you make a change to any, the model will automatically recalc
    everything
    """

    # This does not seem to start it only the commands above work
    # Nor does format seem to work
    # https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s:$(levelname)s:%(message)s')
    logging.debug('Start logging')

    model = Model('test')

    model.population = Population(model)
    model.resource = Resource(model)
    model.economy = Economy(model)
    model.disease = Disease(model)

    # create the resource object that is p populations and n items
    print('resource labels:',
          model.resource.ra_df.index,
          model.resource.ra_df.columns)

    print('model population labels', model.population.attr_pd_df.index)
    print('model level name', model.population.consumption_pl_df.index)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    population_df = model.population.attr_pd_df
    print('Population\n', population_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    population_to_level_pl_df = model.population.consumption_pl_df
    print('Usage by population\n', population_to_level_pl_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    level_to_demand_ln_df = model.population.consumption_ln_df
    print('Usage by level\n', level_to_demand_ln_df)

    # Required equipment is p poulation rows for each resource n
    # which we can get with a mac p x l * l x n
    print('populatation_to_level_pl_df',
          population_to_level_pl_df.shape)
    print('level_to_demand_ln_df', level_to_demand_ln_df.shape)

    # p x l * l x n -> p x n
    population_demand_pn_df = population_to_level_pl_df @ level_to_demand_ln_df

    print('Population demand for Resources\n',
          population_demand_pn_df)


    # Now it get's easier, this is the per unit value, so multiply by the
    # population and the * with values does an element wise multiplication
    # With different tempos, this will be across all d dimensions

    Total_resource_by_population_df = Unit_resource_by_population_df * Population_df.values
    print('Total resource needed by population\n',
          Total_resource_by_population_df)

    Population_by_essentiality_df = model.essential.from_population_pe.df
    print('Population by essentiality\n', Population_by_essentiality_df)

    Total_resource_by_essentiality_df = Population_by_essentiality_df @ Total_resource_by_population_df
    print('Total resource by essentiality\n',
          Total_resource_by_essentiality_df)

    Cost_per_resource_by_essentiality_df = model.supply.cost_per_resource_en.df
    print('Cost per resource by essentiality\n',
          Cost_per_resource_by_essentiality_df)
    
    Total_cost_by_essentiality_df = Total_resource_by_essentiality_df * Cost_per_resource_by_essentiality_df.values
    print('Total cost per resource by essentiality\n',
          Total_cost_by_essentiality_df)

    Stockpile_required_by_essentiality_df = model.stockpile.stockpile_en_df
    print('Stockpile per resource required by essentiality\n',
          Stockpile_required_by_essentiality_df)

    Total_stockpile_by_essentiality_df = Total_resource_by_essentiality_df * Stockpile_required_by_essentiality_df.values
    print('Total Stockpile required by essentiality\n',
          Total_stockpile_by_essentiality_df)


if __name__ == "__main__":
    main()
