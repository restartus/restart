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
import argparse
# name collision https://docs.python.org/3/library/resource.html
# so can't use resource.py
from util import Log
from pathlib import Path

# from config import Config
from loader.load_yaml import LoadYAML
from model import Model
from resourcemodel import Resource
from population import Population
from economy import Economy
from disease import Disease
from behavioral import Behavioral
from mobility import Mobility
from base import Base
from dashboard import Dashboard
from typing import Optional


# This is the only way to get it to work needs to be in main
# https://www.programcreek.com/python/example/192/logging.Formatter
# the confit now seems to work

# log = set_logger(__name__, level=logging.DEBUG)
log = logging.getLogger(__name__)

# https://docs.python.org/3/howto/logging-cookbook.html
log.debug(f"{__name__=}")
log.info("hello world")


def main() -> Model:
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
    # set up the logging
    name = "main"
    log_root = Log(name)
    # Set all the loggers the same
    log = log_root.log
    # test that logging works
    log_root.test(log)

    parser = get_parser()
    args = parser.parse_args()
    log.debug(f"{args=}")
    print(f"{args=}")
    if args.load == "yaml":
        loaded = LoadYAML(args.input, log_root=log_root)
        if not loaded.data:
            raise ValueError("f{args.input=} is empty")
        log.debug(f"{loaded.data=}")
    else:
        raise ValueError("not implemented")

    # refactor with method chaining but this does require a single class
    # and a set of decorators
    model = (
        Model(name, log_root=log_root)
        .configure(loaded)
        .set_population(type=args.population)
        .set_resource(type=args.resource)
        .set_consumption(type=args.consumption)
        .set_economy(type=args.economy)
        .set_disease(type=args.disease)
        .set_mobility(type=args.mobility)
        .set_behavioral(type=args.behavioral)
    )
    # run the loader and put everything into a super dictionary
    # To change the model, just replace LoadYAML and the configuration
    # of it which starts off the entire model

    model1 = old_model(name, log_root=log_root)
    log.debug(f"{model1=}")

    # http://net-informations.com/python/iq/instance.htm
    log.debug(f"{model} is {vars(model)}")
    for name, value in vars(model).items():
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
        # if issubclass(value, Base):
        if isinstance(value, Base):
            log.debug(f"object {name} holds {value} subclass of Base")

    # model.resource.set_stockpile(model.population.level_total_demand_ln_df)
    # log.debug("Safety stock\n%s", model.resource.safety_stock_ln_df)

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

    # test iteration
    for base_key, base_value in model:
        log.debug(f"{base_key=}")
        log.debug(f"{base_value=}")
        for df_key, df_value in base_value:
            log.debug(f"{df_key=}")
            log.debug(f"{df_value=}")

    for s in [3, 6, 9]:
        log.info(f"changing stockpile to {s=}")
        model.resource.set_stockpile_days(s)
        log.info(f"{model.resource.safety_stock_ln_df=}")
        log.info(f"{model.resource.inventory_ln_df=}")

    # run with streamlit run and then this will not return until after
    # when run as just regular python this doesn't do anything
    Dashboard(model, log_root=log_root)

    return model


def get_parser():
    """Set Parser arguments.

    For all the choices
    """
    # expect a real file
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--load",
        choices=["yaml", "csv"],
        default="yaml",
        help="Select loader",
    )
    parser.add_argument(
        "-p",
        "--population",
        choices=["dict", "oes"],
        help="Select population data cube",
    )
    parser.add_argument(
        "-r",
        "--resource",
        choices=["eoc", "chelsea"],
        default="eoc",
        help="Select Resource model",
    )
    parser.add_argument(
        "-c",
        "--consumption",
        choices=["wa-doh", "ensemble"],
        default="wa-doh",
        help="Select Resource model",
    )
    parser.add_argument(
        "-e",
        "--economy",
        choices=["ml", "ensemble"],
        default="ml",
        help="Select Econometric model",
    )
    parser.add_argument(
        "-b",
        "--behavioral",
        choices=["apple", "google", "ensemble"],
        default="ensemble",
        help="Select Econometric model",
    )

    parser.add_argument(
        "-m",
        "--mobility",
        choices=["apple", "ensemble", "google"],
        default="ensemble",
        help="Select Mobility Model",
    )

    parser.add_argument(
        "-d",
        "--disease",
        choices=["imhe", "ensemble", "jhu"],
        default="imhe",
        help="Select Epidemological Disease Model",
    )

    # https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/
    parser.add_argument(
        "input",
        nargs='?',  # one argument
        type=Path,
        default=Path("washington").absolute()
    )
    return parser


def old_model(name, log_root: Optional[Log] = None):
    """Old Model invocation.

    Old Model
    """
    # https://www.tutorialspoint.com/Explain-Python-class-method-chaining
    log.info("creating Model")
    model: Model = Model(name, log_root=log_root)
    # run the loader and put everything into a super dictionary
    # To change the model, just replace LoadYAML and the configuration
    # of it which starts off the entire model
    loaded = LoadYAML(Path("washington").absolute(), log_root=log_root,)
    log.debug(f"{loaded.data=}")
    log.info("configure Model")
    model.configure(loaded)
    # note we cannot just past model down to allow chaining to work
    log.info("creating Population")
    model.population = Population(model.data, log_root=model.log_root)
    log.debug("creating Resource")
    model.resource = Resource(model.data, log_root=model.log_root)
    log.debug("creating Economy")
    model.economy = Economy(model.data, log_root=model.log_root)
    log.debug("creating Disease")
    model.disease = Disease(model.data, log_root=model.log_root)
    log.debug("creating Mobility")
    model.mobility = Mobility(model.data, log_root=model.log_root)
    log.debug("creating Behavioral")
    model.behavioral = Behavioral(model.data, log_root=model.log_root)
    log.debug(f"{model=}")


if __name__ == "__main__":
    main()
