"""Restart.us Main Module.

Eventually this will become a class and we will
keep the constants like names as private class variables

https://stackoverflow.com/questions/20309456/call-a-function-from-another-file-in-python

"""

import argparse

# https://stackoverflow.com/questions/47561840/python-how-can-i-separate-functions-of-class-into-multiple-files
# explains that you can split a class into separate files by
# putting these inside the class definition
# http://effbot.org/pyfaq/how-do-i-share-global-variables-across-modules.htm
# Before we move to full modules, just import locally
# https://inventwithpython.com/blog/2012/04/06/stop-using-print-for-debugging-a-5-minute-quickstart-guide-to-pythons-logging-module/
import logging  # noqa:F401
from pathlib import Path
from typing import Optional

from activity import Activity
from base import Base
from behavioral import Behavioral
from dashboard import Dashboard
from demand import Demand
from disease import Disease

# from population import Population
from economy import Economy

# from config import Config
from load_yaml import LoadYAML
from model import Model
from population_dict import PopulationDict
from resourcemodel import Resource

# name collision https://docs.python.org/3/library/resource.html
# so can't use resource.py
from util import Log

# This is the only way to get it to work needs to be in main
# https://www.programcreek.com/python/example/192/logging.Formatter
# the confit now seems to work


class Compose:
    """Compose an entire model together.

    Note this must be rentrant for streamlit to work
    So it detects if it has been called again
    """

    def __init__(self):
        """Bootstrap the whole model creating all objects.

        Bootstrap where each modules successively knows more about the world
        Population defines Pop_details[p,d], Pop_levels[p,l]

        In this version, there is a specific order of creation and implicit
        dependencies so use in this order. The notation we uses suffixes each
        with a unique letter that gives the number of elements so n x a means n
        resource by a attributes. And yes this will not work when we have more
        than 26 types of dimensions :-)

        In a future revision, you can do this in any order and it will work
        - model itself
        - resource which creates the n resources (eg N95, test kit, etc.) with
          the columns being x attributes like the units and space R[n, x].
        - demand to create burn rates for each "level" of the model.
          Instead of calculating unique burn rates per population element, we
          bucketize with the demand level l so it returns C[l, n]

        TODO: Note that then when running streamlit this will be run multiple
        times and must be reentrant which is not today, the logging does not
        work

        And if you make a change to any, the model will automatically recalc
        everything
        """
        # set up the logging
        # This name should *not* be the same as any module name like main
        name = "test"
        # this should only get run once so check here
        # breakpoint()
        log_root = Log(name)
        # Set all the loggers the same
        log = log_root.log
        # There is a root logger we cannot shutoff so turn off propagation
        log.propagate = False
        # test that logging works
        log_root.test(log)
        # removin this line was the problem but it is back in util.py
        # log.setLevel(logging.DEBUG)

        # do not need this with log_root
        # log = set_logger(__name__, level=logging.DEBUG)
        # log = logging.getLogger(__name__)

        #  https://docs.python.org/3/howto/logging-cookbook.html
        log.debug(f"{__name__=}")
        log.info("hello world")

        parser = self.get_parser()
        args = parser.parse_args()
        log.debug(f"{args=}")
        if args.load == "yaml":
            loaded = LoadYAML(args.input, log_root=log_root)
            if not loaded.data:
                raise ValueError("f{args.input=} is empty")
            log.debug(f"{loaded.data=}")
        else:
            raise ValueError("not implemented")

        # refactor with method chaining but this does require a single class
        # and a set of decorators
        self.model = model = (
            Model(name, log_root=log_root)
            .set_configure(loaded)
            .set_filter(
                county=args.county, state=args.state, population=args.subpop
            )
            .set_population(type=args.population)
            # .set_population(type=args.students)
            .set_resource(type=args.resource)
            # .set_resource(type=args.pharma)
            .set_demand(type=args.demand)
            .set_economy(type=args.economy)
            .set_disease(type=args.disease)
            .set_activity(type=args.activity)
            .set_behavioral(type=args.behavioral)
        )
        # run the loader and put everything into a super dictionary
        # To change the model, just replace LoadYAML and the configuration
        # of it which starts off the entire model
        self.model1 = self.old_compose("old_" + name, log_root=log_root)
        log.debug(f"{self.model1=}")

        # http://net-informations.com/python/iq/instance.htm
        log.debug(f"{model} is {vars(model)}")
        for name, value in vars(model).items():
            # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
            # if issubclass(value, Base):
            if isinstance(value, Base):
                log.debug(f"object {name} holds {value} subclass of Base")

        # model.resource.set_inv_min(model.population.level_total_demand_ln_df)
        # log.debug("Safety stock\n%s", model.resource.safety_stock_ln_df)

        # create the resource object that is p populations and n items
        log.debug("resource attributes\n%s", model.resource.attr_na_df)

        # This is a population p by d dimension, eventually the second column
        # should be a call back that calculates demand based
        # Eventually, this will be multi dimenstional, so in addition to the
        # total but there will also be the number of COVID patients And other
        # tempo data like number of runs so eventually this is d dimensinoal
        log.debug("Population\n%s", model.population.detail_pd_df)

        # Now bucket population into a set of levels
        # So we have a table is p x l
        log.debug("Population by level\n%s", model.demand.level_pl_df)

        # This is rows that are levels adn then usage of each resource  or l, n
        # When population become n x d, then there will be a usage
        # level for each do, so this become d x p x n
        log.debug(f"{model.demand.level_demand_ln_df=}")

        # p x l * l x n -> p x n
        log.debug(f"{model.demand.demand_pn_df=}")

        # Now it get's easier, this is the per unit value, so multiply by the
        # population and the * with values does an element wise multiplication
        # With different tempos, this will be across all d dimensions

        log.debug(f"{model.demand.total_demand_pn_df=}")
        log.debug(f"{model.demand.level_pl_df=}")

        log.debug(f"{model.resource.cost_ln_df=}")

        # model.demand.level_total_cost(model.resource.cost_ln_df)
        # log.debug(f"{model.demand.level_total_cost_ln_df=}")

        # test iteration
        for base_key, base_value in model:
            log.debug(f"{base_key=}")
            log.debug(f"{base_value=}")
            for df_key, df_value in base_value:
                log.debug(f"{df_key=}")
                log.debug(f"{df_value=}")

        for s in [30, 60, 90]:
            log.critical(f"changing stockpile to {s=}")
            log.critical(f"{model.demand.level_total_demand_ln_df=}")
            model.resource.set_inv_min(
                model.demand.level_total_demand_ln_df, s
            )
            log.debug(f"{model.resource.safety_stock_ln_df=}")
            log.critical(f"{model.resource.inventory_ln_df=}")

        # run with streamlit run and then this will not return until after
        # when run as just regular python this doesn't do anything
        log.info("start dashboard ")
        log.debug("start dashboard")

    def get_parser(self):
        """Set Parser arguments.

        For all the choices, returns an argparser object
        """
        # TODO: Convert to using confuse to store parameters
        # or maybe the configargparser
        # https://github.com/beetbox/confuse
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

        parser.add_argument("--county", help="Select county")

        parser.add_argument("--state", help="Select state")

        parser.add_argument(
            "--subpop", help="Select subpopulation of interest"
        )

        parser.add_argument(
            "-r",
            "--resource",
            choices=["dict", "who", "eoc", "chelsea"],
            default="dict",
            help="Select Resource model",
        )

        parser.add_argument(
            "-c",
            "--demand",
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
            "--activity",
            choices=["apple", "ensemble", "google"],
            default="ensemble",
            help="Select Activity Model",
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
            "-i", "--input", type=Path, default=Path("config").absolute(),
        )
        return parser

    def old_compose(self, name, log_root: Optional[Log] = None):
        """Old Model invocation.

        Old Model composition in parts not using chaining
        """
        # https://www.tutorialspoint.com/Explain-Python-class-method-chaining
        if log_root is not None:
            log = log_root.log
        else:
            log = logging.getLogger(__name__)

        log.info("creating Model")
        model: Model = Model(name, log_root=log_root)
        # run the loader and put everything into a super dictionary
        # To change the model, just replace LoadYAML and the configuration
        # of it which starts off the entire model
        loaded = LoadYAML(Path("washington").absolute(), log_root=log_root,)
        log.debug(f"{loaded.data=}")
        log.info("configure Model")
        model.set_configure(loaded)
        # note we cannot just past model down to allow chaining to work
        log.info("creating Population")
        model.population = PopulationDict(
            model.data,
            model.label,
            index="Population p",
            columns="Pop Detail d",
            log_root=log_root,
        )
        log.debug("creating Resource")
        model.resource = Resource(model.data, log_root=model.log_root)
        log.debug("creating Demand")
        model.demand = Demand(model.data, log_root=model.log_root)
        # log.debug("creating Filter")
        # model.filter = Filter(model.data, log_root=model.log_root)
        log.debug("creating Economy")
        model.economy = Economy(model.data, log_root=model.log_root)
        log.debug("creating Disease")
        model.disease = Disease(model.data, log_root=model.log_root)
        log.debug("creating Activity")
        model.activity = Activity(model.data, log_root=model.log_root)
        log.debug("creating Behavioral")
        model.behavioral = Behavioral(model.data, log_root=model.log_root)
        log.debug(f"{model=}")


# This is a global variable so easy to find
# this does not work, streamlit just runs the whole things all over again for
# each page
# compose: Optional[Compose] = None

if __name__ == "__main__":
    # compose the entire model runs as a class so it is rentrant
    compose = Compose()
    Dashboard(compose.model)
