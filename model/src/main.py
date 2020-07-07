"""Restart.us Main Module.

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
import logging  # noqa:F401

# name collision https://docs.python.org/3/library/resource.html
# so can't use resource.py
from util import Log
from config import Config
from model import Model
from resourcemodel import Resource
from population import Population
from economy import Economy
from disease import Disease
from behavioral import Behavioral
from base import Base

# This is the only way to get it to work needs to be in main
# https://www.programcreek.com/python/example/192/logging.Formatter
# the confit now seems to work

# log = set_logger(__name__, level=logging.DEBUG)
log = logging.getLogger(__name__)

# https://docs.python.org/3/howto/logging-cookbook.html
log.debug(f"name {__name__}")
log.info("hello world")


def main():
    """Bootstrap the whole model creating all objects.

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
    global log
    name = "main"
    # set up the logging
    log_root = Log(name)
    # Set all the loggers the same
    log = log_root.log
    # test that logging works
    log_root.test(log)

    # run the configuration load
    config = Config(
        "config.yaml",
        "data.yaml",
        "model.yaml",
        "description.yaml",
        log_root=log_root,
    )
    log.debug(f"{config.dict=}")

    # Static typing for custom classes
    log.info("creating Model")
    model: Model = Model(name, config, log_root=log_root)
    log.info("creating Population")
    model.population: Population = Population(model)
    log.debug("creating Resource")
    model.resource: Resource = Resource(model)
    log.debug("creating Economy")
    model.economy: Economy = Economy(model)
    log.debug("creating Disease")
    model.disease: Disease = Disease(model)
    log.debug("creating Behavioral")
    model.behavioral: Behavioral = Behavioral(model)

    # http://net-informations.com/python/iq/instance.htm
    log.debug(f"{model} is {vars(model)}")
    for name, value in vars(model).items():
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
        # if issubclass(value, Base):
        if isinstance(value, Base):
            log.debug(f"object {name} holds {value} subclass of Base")

    model.resource.set_stockpile(model.population.level_total_demand_ln_df)
    log.debug("Safety stock\n%s", model.resource.safety_stock_ln_df)

    # create the resource object that is p populations and n items
    log.debug("resource attributes\n%s", model.resource.attr_na_df)

    # This is a population p by d dimension, eventually the second column
    # should be a call back that calculates consumption based
    # Eventually, this will be multi dimenstional, so in addition to the total
    # but there will also be the number of COVID patients
    # And other tempo data like number of runs so
    # eventually this is d dimensinoal
    log.debug("Population\n%s", model.population.attr_pd_df)

    # Now bucket population into a set of levels
    # So we have a table is p x l
    log.debug("Population by level\n%s", model.population.level_pl_df)

    # This is rows that are levels adn then usage of each resource  or l, n
    # When population become n x d, then there will be a usage
    # level for each do, so this become d x p x n
    log.debug("level demand\n%s", model.population.level_demand_ln_df)

    # p x l * l x n -> p x n
    log.debug(
        "Population demand for Resources\n%s", model.population.demand_pn_df
    )

    # Now it get's easier, this is the per unit value, so multiply by the
    # population and the * with values does an element wise multiplication
    # With different tempos, this will be across all d dimensions

    log.debug(
        "Population Total Demand\n%s", model.population.total_demand_pn_df
    )

    log.debug("Population by level\n%s", model.population.level_pl_df)

    log.debug(
        "Cost per resource by population level\n%s", model.resource.cost_ln_df
    )

    model.population.level_total_cost(model.resource.cost_ln_df)
    log.debug(
        "Population by level Total cost\n%s",
        model.population.level_total_cost_ln_df,
    )

    for s in [3, 6, 9]:
        log.info(f"changing stockpile to {s=}")
        model.resource.set_stockpile_days(model, s)
        log.info(f"{model.resource.safety_stock_ln_df=}")
        log.info(f"{model.resource.inventory_ln_df=}")
    return model


if __name__ == "__main__":
    main()
