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

from base import Base
from dashboard import Dashboard
from log import Log
from model import Model
from util import set_config


class Compose:
    """Compose an entire model together.

    Note this must be rentrant for streamlit to work
    So it detects if it has been called again
    """

    def __init__(self):
        """Bootstrap the whole model creating all objects.

        Bootstrap where each modules successively knows more about the world

        In this version, there is a specific order of creation and implicit
        dependencies so use in this order. The notation we uses suffixes each
        different meanings.

        The major model elements are:
        Real World Objects
        Population - People and their attributes
        Organization - Hospitals, EMTs, etc.
        Resources - PPE, Testing, Lab Capacity,...
        Warehouse - Storing resources

        Transformation Objects: These map from real to real
        Demand - The demand from Populations and Organizations for Resources

        Notation: We use snake_case to bind these together

        Object_<dimension description...>_units_dimensions_type

        For example: this means population object as a total count (vs per
        unit) with dimensions:
        g - geo. These are normally filtered out to get to the right level
        t - time. These are normally filtered so it is a single dimension
        r - range of estimates. by default just a single point estimate but can
            be as many different points as you need with lo, mid, hi typically
        p - population one for each class. Note that each object can have
            different summary levels, so p = p0 and l = p1 so the first level
            summary. We allow an unlimited levels, but a single variable with a
            number indicates how much summarization with 0 being the most
            detailed.
        d - a shortcut for the "columns" that describe it for this,
            the last element also called the longer form of this is P0 for the
            first level then P1,... as you summarize more. Because python
            doesn't support the "hat" used in the equations hat{p} becomes a
            capital letter P.

        We normally use the shortest notation but all these are valid
        and should point to the same object. With the most common notation just
        noting the object_units_lastdimension_type.

        The notation used here is not full Latex. Use the
        [README.md](README.tex.md) to see the full notation or the Jupyter
        notebook for the long descriptions.

        Pop_tot_desc_gtrpd_df == Pop_tot_gtrpd_df == Pop_tot_gtrp0phat_df ==
        Population_total_description_gtrp0P0_df ==
        Population_geo_time_range_detail_description_detail_gtrp0P0_dataframe

        Summarization levels. Each of these dimensions has a hierarchy:
        As an example with population, population details pd, but you also have
        a summary level population level l, this is a shorthand for where you
        can map say all the SOC or NAICS codes for healthcare professions or
        companies into healthcare. The normal notation for this is

        """
        # set up the logging
        # This name should *not* be the same as any module name like main
        name = "model"
        self.log_root = Log(name)
        log = self.log = self.log_root.log
        # There is a root logger we cannot shutoff so turn off propagation
        log.propagate = False
        # test that logging works
        #  https://docs.python.org/3/howto/logging-cookbook.html
        self.log_root.test(log)
        log.debug(f"{__name__=}")  # goes to log file
        log.info("hello world")  # goes to console

        parser = self.create_parser()
        args = parser.parse_args()
        log.debug(f"{args=}")

        # move config init here so that it can access args
        # now set_configure is just used to change the base default
        self.config = set_config(args.config)
        # self.config = confuse.Configuration("config")
        # Arguments can use dot notation to change
        # Anything in the yaml file
        # https://confuse.readthedocs.io/en/latest/
        self.config.set_args(args, dots=True)

        # uses method chaining
        self.model = model = (
            Model(name, log_root=self.log_root)
            .set_configure(self.config)
            .set_filter(
                county=args.county, state=args.state, subpop=args.subpop
            )
            .set_population(type=args.population)
            .set_organization(type=args.organization)
            .set_resource(type=args.resource)
            .set_inventory(type=args.inventory)
            .set_demand(type=args.demand)
            .set_economy(type=args.economy)
            .set_disease(type=args.disease)
            .set_activity(type=args.activity)
            .set_behavioral(type=args.behavioral)
            .set_output(out=args.output, csv=args.csv)
        )
        # run the loader and put everything into a super dictionary
        # To change the model, just replace LoadYAML and the configuration
        # of it which starts off the entire model
        # TODO: confuse breaks the old model
        # self.model1 = self.old_compose("old_" + name, log_root=log_root)
        # log.debug(f"{self.model1=}")

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

        # test iteration
        for base_key, base_value in model:
            log.debug(f"{base_key=}")
            log.debug(f"{base_value=}")
            for df_key, df_value in base_value:
                log.debug(f"{df_key=}")
                log.debug(f"{df_value=}")

        # this just keeps increasing supply also test decreasing
        for s in [30, 60, 90, 40, 20]:
            log.debug("reset inventory to minimum")
            model.resource.demand(model.resource.inventory_ln_df)
            log.critical(f"changing stockpile to {s=}")
            log.debug(f"{model.demand.level_total_demand_ln_df=}")
            model.resource.set_inv_min(
                model.demand.level_total_demand_ln_df, s
            )
            log.debug(f"{model.resource.inv_min_rln_df=}")
            log.critical(f"{model.resource.inventory_ln_df=}")

        # run with streamlit run and then this will not return until after
        # when run as just regular python this doesn't do anything
        log.info("start dashboard ")
        log.debug("start dashboard")

    def create_parser(self):
        """Set Parser arguments.

        For all the choices, returns an argparser object for use by confuse
        """
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-p",
            "--population",
            default="dict",
            choices=["dict", "oes", "wa"],
            help="Select population data cube",
        )

        parser.add_argument(
            "--organization", default="dict", help=["dict", "ca"]
        )

        parser.add_argument("--csv", help="Select CSV file output")

        parser.add_argument("--county", help="Select county")

        parser.add_argument("--state", help="Select state")

        parser.add_argument(
            "--subpop", help="Select subpopulation of interest"
        )

        parser.add_argument(
            "--config", default=".", help="Select path to config.yaml"
        )

        parser.add_argument("--output", "-o", help="Write results to CSV file")

        parser.add_argument(
            "-r",
            "--resource",
            choices=["dict", "who", "eoc", "chelsea"],
            default="dict",
            help="Select Resource model",
        )

        parser.add_argument(
            "-i",
            "--inventory",
            choices=["dict"],
            default="dict",
            help="Select inventory model",
        )

        parser.add_argument(
            "-c",
            "--demand",
            choices=["mitre", "jhu", "washington", "dict"],
            default="dict",
            help="Select Demand model",
        )
        parser.add_argument(
            "-e",
            "--economy",
            choices=["dict", "ml", "ensemble"],
            default="dict",
            help="Select Econometric model",
        )
        parser.add_argument(
            "-b",
            "--behavioral",
            choices=["dict", "apple", "google", "ensemble"],
            default="dict",
            help="Select Econometric model",
        )

        parser.add_argument(
            "-m",
            "--activity",
            choices=["dict", "apple", "ensemble", "google"],
            default="dict",
            help="Select Activity Model",
        )

        parser.add_argument(
            "-d",
            "--disease",
            choices=["dict", "imhe", "ensemble", "jhu"],
            default="dict",
            help="Select Epidemological Disease Model",
        )

        return parser

    '''
    # confuse breaks the old model so need to go and fix this
    # deprecated
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
    '''


if __name__ == "__main__":
    # TODO: longer term we will run a series of models
    # compose the entire model runs as a class so it is rentrant
    compose = Compose()
    Dashboard(compose.model)
