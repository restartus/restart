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
from typing import List

from base import Base

# Use jupyter voila instead
# from dashboard import Dashboard
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
        p1 - a shortcut for the "columns" that describe it for this,
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
        self.parameter = self.config["Parameter"]

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
            .set_financial(type=args.financial)
            .set_mobility(type=args.mobility)
            .set_epi(type=args.epi)
            .set_output(out=args.output, csv=args.csv)
        )
        # run the loader and put everything into a super dictionary
        # To change the model, just replace LoadYAML and the configuration
        # of it which starts off the entire model

        # http://net-informations.com/python/iq/instance.htm
        log.debug(f"{model=} is {vars(model)=}")
        for name, value in vars(model).items():
            # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
            # if issubclass(value, Base):
            if isinstance(value, Base):
                log.debug(f"object {name} holds {value} subclass of Base")

        # test iteration
        for base_key, base_value in model:
            log.debug(f"{base_key=}")
            log.debug(f"{base_value=}")
            for df_key, df_value in base_value:
                log.debug(f"{df_key=}")
                log.debug(f"{df_value=}")

        # TODO: when the rest of the world uses ranges we don't need to this
        # but we need rp1n not p1n, so just stack this
        log.debug("setting average orders")
        model.inventory.set_average_orders_per_period(
            model.demand.demand_by_popsum1_total_rp1n_tc
        )
        log.debug(f"{model.demand.demand_by_popsum1_total_rp1n_tc.df=}")
        # this just keeps increasing supply also test decreasing
        # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        # fill up the entire range no matter how there are
        backstop_list: List = self.parameter["backstop"].get()
        range_len = model.inventory.inv_by_popsum1_total_rp1n_tc.array.shape[0]
        for index in range(0, len(backstop_list), range_len):
            # note on the :, Black and flake8 are fighting
            backstop = backstop_list[index : index + range_len]  # noqa:E203
            log.critical(f"changing days of backstop to {backstop=}")
            log.debug("reset inventory to zero by ordering everything")
            model.inventory.order(model.inventory.inv_by_popsum1_total_rp1n_tc)
            model.inventory.set_min_in_periods(backstop)
            log.debug(f"{model.inventory.inv_by_popsum1_total_rp1n_tc.df=}")

        # run with streamlit run and then this will not return until after
        # when run as just regular python this doesn't do anything
        log.info("start dashboard ")
        log.debug("start dashboard")

    def create_parser(self):
        """Set Parser arguments.

        For all the choices, returns an argparser object for use by confuse
        """
        # TODO: remove all defaults and set them in the config file
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-p",
            "--population",
            choices=["dict", "oes", "wa"],
            default="dict",
            help="Select population data cube",
        )

        parser.add_argument("--organization", help=["dict", "ca"])

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
            "-d",
            "--demand",
            choices=["mitre", "jhu", "population", "organization"],
            default="population",
            help="Select Demand model",
        )
        parser.add_argument(
            "-f",
            "--financial",
            choices=["dict", "ml", "ensemble"],
            default="dict",
            help="Select Financial model",
        )
        parser.add_argument(
            "-m",
            "--mobility",
            choices=["dict", "apple", "google", "ensemble"],
            default="dict",
            help="Select mobility  model",
        )

        parser.add_argument(
            "-e",
            "--epi",
            choices=["dict", "imhe", "ensemble", "jhu"],
            default="dict",
            help="Select Epi Model",
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
        log.debug("creating Financial")
        model.financial = Financial(model.data, log_root=model.log_root)
        log.debug("creating Epi")
        model.epi = Epi(model.data, log_root=model.log_root)
        log.debug("creating Mobility")
        model.mobility = Mobility(model.data, log_root=model.log_root)
        log.debug(f"{model=}")
    '''


if __name__ == "__main__":
    # compose the entire model runs as a class so it is rentrant
    compose = Compose()
    # Abandon dashboard, use voila and vuetify
    # Dashboard(compose.model)
