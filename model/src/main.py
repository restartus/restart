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
from model import Model
from resource import Resource
from consumption import Consumption
from population import Population
from essential import Essential
from supply import Supply


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
    model = Model('test')
    model.resource = Resource(model)
    model.consumption = Consumption(model)
    model.population = Population(model)
    # returns p population, d details and l levels of protection
    model.essential = Essential(model)
    model.supply = Supply(model)

    print('model resource labels', model.label["Resource"])

    # create the resource object that is p populations and n items
    print('resource labels:',
          model.resource.ra_df.index,
          model.resource.ra_df.columns)

    print('model population labels', model.population.detail_pd_df.index)
    print('model level name', model.population.consumption_pl_df.index)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    Population_df = model.population.detail_pd_df
    print('Population\n', Population_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    Levels_by_population_df = model.population.consumption_pl_df
    print('Usage by population\n', Levels_by_population_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    Usage_by_level_df = model.consumption.ln_df
    print('Usage by level\n', Usage_by_level_df)

    # Required equipment is p poulation rows for each resource n
    # which we can get with a mac p x l * l x n
    print('levels_by_population_df',
          Levels_by_population_df.shape)
    print('usage_by_level_df', Usage_by_level_df.shape)

    # p x l * l x n -> p x n
    Unit_resource_by_population_df = Levels_by_population_df @ Usage_by_level_df

    print('Unit Resources needed by population\n',
          Unit_resource_by_population_df)
    # now convert to a dataframe

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

    Cost_per_resource_by_essentiality_df = model.essential.cost_per_resource_en.df
    print('Cost per resource by essentiality\n',
          Cost_per_resource_by_essentiality_df)
    
    Total_cost_by_essentiality_df = Total_resource_by_essentiality_df * Cost_per_resource_by_essentiality_df.values
    print('Total cost per resource by essentiality\n',
          Total_cost_by_essentiality_df)

    Stockpile_required_by_essentiality_df = model.essential.stockpile_en_df
    print('Stockpile per resource required by essentiality\n',
          Stockpile_required_by_essentiality_df)

    Total_stockpile_by_essentiality_df = Total_resource_by_essentiality_df * Stockpile_required_by_essentiality_df.values
    print('Total Stockpile required by essentiality\n',
          Total_stockpile_by_essentiality_df)


if __name__ == "__main__":
    main()
