"""Restart.us Main Module.

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
"""
from resource import resource_name

from consumption0 import level_by_population, level_name, usage_by_level
from essential import essential_name, population_by_essentiality
from population0 import population, population_label
from supply import (
    cost_per_resource_by_essentiality,
    stockpile_required_by_essentiality,
)


# https://www.w3schools.com/python/python_classes.asp
class Model:
    """Set Main Model."""

    def __init__(
        self, resource_name, population_label, level_name, essential_name
    ):
        """Initialize Main."""
        self.resource_name = resource_name
        # population has population rows details
        self.population_label = population_label
        self.level_name = level_name
        self.essential_name = essential_name


def main():
    """Set Main boot."""
    print("hello world")
    model = Model(
        resource_name(), population_label(), level_name(), essential_name()
    )
    print("model resource name\n", model.resource_name)
    print("model population label\n", model.population_label)
    print("model level name\n", model.level_name)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    Population_df = population(model)
    print("Population\n", Population_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    Levels_by_population_df = level_by_population(model)
    print("Usage by population\n", Levels_by_population_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    Usage_by_level_df = usage_by_level(model)
    print("Usage by level\n", Usage_by_level_df)

    # Required equipment is p poulation rows for each resource n
    # which we can get with a mac p x l * l x n
    print("levels_by_population_df", Levels_by_population_df.shape)
    print("usage_by_level_df", Usage_by_level_df.shape)

    # p x l * l x n -> p x n
    Unit_resource_by_population_df = (
        Levels_by_population_df @ Usage_by_level_df
    )

    print(
        "Unit Resources needed by population\n", Unit_resource_by_population_df
    )
    # now convert to a dataframe

    # Now it get's easier, this is the per unit value, so multiply by the
    # population and the * with values does an element wise multiplication
    # With different tempos, this will be across all d dimensions

    Total_resource_by_population_df = (
        Unit_resource_by_population_df * Population_df.values
    )
    print(
        "Total resource needed by population\n",
        Total_resource_by_population_df,
    )

    Population_by_essentiality_df = population_by_essentiality(model)
    print("Population by essentiality\n", Population_by_essentiality_df)

    Total_resource_by_essentiality_df = (
        Population_by_essentiality_df @ Total_resource_by_population_df
    )
    print(
        "Total resource by essentiality\n", Total_resource_by_essentiality_df
    )

    Cost_per_resource_by_essentiality_df = cost_per_resource_by_essentiality(
        model
    )
    print(
        "Cost per resource by essentiality\n",
        Cost_per_resource_by_essentiality_df,
    )

    Total_cost_by_essentiality_df = (
        Total_resource_by_essentiality_df
        * Cost_per_resource_by_essentiality_df.values
    )
    print(
        "Total cost per resource by essentiality\n",
        Total_cost_by_essentiality_df,
    )

    Stockpile_required_by_essentiality_df = stockpile_required_by_essentiality(
        model
    )
    print(
        "Stockpile per resource required by essentiality\n",
        Stockpile_required_by_essentiality_df,
    )

    Total_stockpile_by_essentiality_df = (
        Total_resource_by_essentiality_df
        * Stockpile_required_by_essentiality_df.values
    )
    print(
        "Total Stockpile required by essentiality\n",
        Total_stockpile_by_essentiality_df,
    )


if __name__ == "__main__":
    main()
