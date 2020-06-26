""" Restart.us Main Module

 Eventually this will become a class and we will
 keep the constants like names as private class variables

 https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python

"""

# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
# explains that you can split a class into separate files by
# putting these inside the class definition
# http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
# Before we move to full modules, just import locally
# https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
import logging
import numpy as np
import pandas as pd

# name collision https://docs.python.org/3/library/resource.html
# so can't use resource.py
from model import Model
from resourcemodel import Resource
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

    # place holder just 30 days for essential and then zero for the rest
    safety_stock_days_ln_arr = np.array([[30, 30],
                                         [0, 0]])
    safety_stock_days_ln_df = pd.DataFrame(safety_stock_days_ln_arr,
                                           index=model.label["Level"],
                                           columns=model.label["Resource"])

    total_safety_stock_ln_df = model.population.level_total_demand_ln_df * safety_stock_days_ln_df
    LOG.debug('total safety stock %s', total_safety_stock_ln_df)
    model.resource.inventory.safety_stock(total_safety_stock_ln_df)

    # create the resource object that is p populations and n items
    print('resource labels:',
          model.resource.attr_ra_df.index,
          model.resource.attr_ra_df.columns)

    print('model population labels', model.population.attr_pd_df.index)
    print('model level name', model.population.level_pl_df.index)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    print('Population\n', model.population.attr_pd_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    print('Population by level\n', model.population.level_pl_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    print('level demand\n', model.population.level_demand_ln_df)

    # p x l * l x n -> p x n
    assert model.population.demand_pn_df == model.population.level_pl_df @ model.population.level_demand_ln_df

    print('Population demand for Resources\n', model.population.demand_pn_df)

    # Now it get's easier, this is the per unit value, so multiply by the
    # population and the * with values does an element wise multiplication
    # With different tempos, this will be across all d dimensions

    assert model.population.total_demand_pn_df == model.population.demand_pn_df * model.population.attr_pd_df.values
    print('Population Total Demand', model.population.total_demand_pn_df)

    print('Population by level\n', model.population.level_pl_df)

    print('Population Level Total Demand',
          model.population.level_total_demand_ln_df)

    assert model.population.level_total_demand_ln_df == model.population.level_pl_df.T @ model.population.total_demand_pn_df

    print('Population level total demand for resources\n',
          model.population.level_total_demand_ln_df)

    print('ask resrouce for total demand worth of resource')
    model.resource.demand(model.population.level_total_demand_ln_df)

    print('Cost per resource by essentiality\n',
          model.resource.level_cost_ln_df)

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
