"""Model definition.

The model shape is configured here.
And this uses chained methods as decorators
https://www.w3schools.com/python/python_classes.asp
"""
# https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel
# this allows Model to refer to itself
from __future__ import annotations

from typing import Generator, List, Optional, Tuple

from base import Base
from demand import Demand
from demand_dict import DemandDict
from epi import Epi
from epi_dict import EpiDict
from epi_table import EpiTable
from filtermodel import Filter
from financial import Financial
from financial_dict import FinancialDict
from financial_table import FinancialTable
from inventory import Inventory
from inventory_dict import InventoryDict
from log import Log
from mobility import Mobility
from mobility_dict import MobilityDict
from mobility_table import MobilityTable
from organization import Organization
from organization_dict import OrganizationDict
from output import Output

# import numpy as np  # type:ignore
# import pandas as pd  # type:ignore
# from population import Population
from population import Population
from population_dict import PopulationDict
from population_oes import PopulationOES
from population_wa import PopulationWA
from resource_dict import ResourceDict
from resourcemodel import Resource


class Model(Base):
    """Main model for planning.

    They then will create the correct tables for use by the main computation
    This model has pointers to the major elements of the model.

    The model is made up of a series of classes for each of the major model
    elements. Each of the major model elements are based on a class structure
    that are kept in a network of links in the Model class. The Model acts as a
    single global data structure for the entire project.

    It uses chaining so that you can in a single statement set all the modeling
    elements. These include:

    Real resources. Like Populations or Organizations
    Transforms. Which computes mapping of Population onto say Resources
    Actions. These are things that affect Real Objects like Demand.

    - LogBase. Just for logging so every class that wants to log needs this as
       a base class
    - Base. This has the descriptions baked in. Used to traverse the Model
      class
    when you want to print or interrogate the Model.
    - Resource. Every time you create a new way to read or manage resources,
      base on this. en.utf-8.add
    """

    # https://satran.in/b/python--dangerous-default-value-as-argument
    # https://stackoverflow.com/questions/2…

    # do not do default assignment, it remembers it on eash call
    # https://docs.python.org/3/library/typing.html
    def __init__(self, name, log_root: Optional[Log] = None):
        """Initialize the model."""
        # the long description of each
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"{__name__=}")

        self.name: str = name
        if not log.hasHandlers():
            print(f"{log=} has no handlers")
        log.debug(f"{self.name=}")

    def set_configure(self, config) -> Model:
        """Configure the Model.

        Uses Loaded as a dictionary and puts it into model variables
        """
        log = self.log
        self.config = config
        log.debug(f"{self.config=}")

        return self

    # TODO: This should be a generated set of methods as they are all identical
    def set_population(self, type: str = None) -> Model:
        """Create population class for model.

        Population created here
        """
        # the old method
        # self.population = Population(
        #    self.data, log_root=self.log_root, type=type
        # )
        # the super class population uses type to return the exact model
        # filter is by happens after this
        self.population: Population

        if type == "oes":
            self.population = PopulationOES(
                self.config,
                self.filter,
                log_root=self.log_root,
            )
        elif type == "wa":
            self.population = PopulationWA(
                self.config, self.filter, log_root=self.log_root
            )
        elif type == "dict":
            # change this to the the naming of columns
            self.population = PopulationDict(
                self.config,
                log_root=self.log_root,
            )
        else:
            raise ValueError(f"{type=} not implemented")
        return self

    def set_organization(self, type: str = None) -> Model:
        """Set organization."""
        self.organization: Organization
        if type == "dict":
            self.organization = OrganizationDict(
                self.config, log_root=self.log_root
            )

        return self

    def set_resource(self, type: str = None) -> Model:
        """Create resource class.

        Resource
        """
        self.resource: Resource
        if type == "dict":
            self.resource = ResourceDict(self.config, log_root=self.log_root)
        return self

    def set_inventory(self, type: str = None) -> Model:
        """Create Inventory management for a specific warehouse."""
        self.inventory: Inventory
        if type == "dict":
            self.inventory = InventoryDict(self.config, log_root=self.log_root)
        return self

    def set_demand(self, type: str = None) -> Model:
        """Set demand.

        Demand by population levels l
        """
        log = self.log
        self.demand: Demand
        if type == "mitre":
            log.debug("Use Mitre demand")
            raise ValueError("{type=} not implemented")
        elif type == "jhu":
            log.debug("Use JHU burn rate model")
            raise ValueError("{type=} not implemented")
        else:
            log.debug("Use default yaml dictionary data")
            self.demand = DemandDict(
                self.config,
                res=self.resource,
                pop=self.population,
                log_root=self.log_root,
                type=type,
            )
        return self

    def set_filter(
        self, county: str = None, state: str = None, subpop: str = None
    ) -> Model:
        """Filter the model.

        Shrink the model to relevant population, resource
        """
        self.filter = Filter(
            log_root=self.log_root,
            county=county,
            state=state,
            subpop=subpop,
        )

        return self

    def set_financial(self, type: str = None) -> Model:
        """Create Financial model.

        Financial creation
        """
        log = self.log
        self.financial: Financial
        if type == "dict":
            self.financial = FinancialDict(
                self.config, log_root=self.log_root, type=type
            )
        elif type == "table":
            self.financial = FinancialTable(
                self.config, log_root=self.log_root, type=type
            )
        else:
            log.error(f"Financial Model {type=} not implemented")
        return self

    def set_epi(self, type: str = None) -> Model:
        """Create Epi model.

        Epi create
        """
        log = self.log
        self.epi: Epi
        if type == "dict":
            self.epi = EpiDict(self.config, log_root=self.log_root, type=type)
        elif type == "table":
            self.epi = EpiTable(self.config, log_root=self.log_root, type=type)
        else:
            log.error(f"Epi Model {type=} not implemented")
        return self

    def set_mobility(self, type: str = None) -> Model:
        """Create Behavior model.

        Behavior create
        """
        log = self.log
        self.mobility: Mobility
        if type == "dict":
            self.mobility = MobilityDict(
                self.config, log_root=self.log_root, type=type
            )
        elif type == "table":
            self.mobility = MobilityTable(
                self.config, log_root=self.log_root, type=type
            )
        else:
            log.error("Behavior not implemented")
        return self

    # https://docs.python.org/3/library/typing.html#typing.Generator
    # returns yield type, send type return type which are null
    def walk(self) -> Generator[Tuple[str, Base], None, None]:
        """Walk through all Base objects in Model.

        This is needed for things like Output which are called by Model
        and you cannot mutually import it. Use a generator instead. Because
        python cannot interpret this correctly.
        """
        log = self.log
        for name, value in self:
            log.debug(f"{name=} {value=}")
            yield name, value

    def set_output(self, out: str = None, csv: str = None) -> Model:
        """Generate output."""
        self.output = Output(
            self.walk,
            config=self.config,
            log_root=self.log_root,
            out=out,
            csv=csv,
        )
        return self

    # https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints
    # https://www.datacamp.com/community/tutorials/python-iterator-tutorial
    # https://towardsdatascience.com/how-to-loop-through-your-own-objects-in-python-1609c81e11ff
    # So we want the iterable to be the Base Class
    # The iterator is Model which can return all the Base classes
    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    def __iter__(self) -> Model:
        """Iterate through the model getting only Base objects."""
        log = self.log
        self.base_list: List = [
            k for k, v in vars(self).items() if isinstance(v, Base)
        ]
        log.debug(f"{self.base_list=}")
        self.base_len: int = len(self.base_list)
        self.base_index: int = 0
        return self

    def __next__(self) -> Tuple[str, Base]:
        """Next Base."""
        log = self.log
        if self.base_index >= self.base_len:
            raise StopIteration
        log.debug(f"{self.base_index=}")
        key = self.base_list[self.base_index]
        value = vars(self)[key]
        log.debug(f"{key=} {value=}")
        self.base_index += 1
        return key, value

    # Use the decorator pattern that Keras and other use with chaining
    def set_logger(self, name: str = __name__) -> Model:
        """Set Log.

        Setup the root logger and log
        """
        self.log_root = Log(name)
        self.log = self.log_root.log
        return self
