"""Define Model definition.

The model shape is configured here.
And this uses chained methods as decorators
https://www.w3schools.com/python/python_classes.asp
"""
# https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel
# this allows Model to refer to itself
from __future__ import annotations

import logging  # noqa: F401
from typing import Dict, List, Optional, Tuple

from activity import Activity
from base import Base
from behavioral import Behavioral
from demand import Demand
from demand_dict import DemandDict
from demand_wa import DemandWA
from disease import Disease
from economy import Economy
from filtermodel import Filter
from modeldata import ModelData

# import numpy as np  # type:ignore
# import pandas as pd  # type:ignore
# from population import Population
from population import Population
from population_dict import PopulationDict
from population_oes import PopulationOES
from resource_dict import ResourceDict
from resourcemodel import Resource
from util import Log


class Model(Base):
    """Main model for planning.

    It sets the dimensionality of the problem and also the names of all the
    elements. Each subsystem will take the dimensions and names as inputs.

    They then will create the correct tables for use by the main computation
    This model has pointers to the major elements of the model.

    Attr:
    name: the friendly string name
    label: This is what structures the entire model with a list of labels
            The defaults are what give us the simplified Bharat model

    These are the name dimensions of each, the length of each is set to
    parameters

    resources: n resources being modeled
        resource Attribute: a attributes for a resource
    population: p labels defines the populations
        population Details: d details about each population
        protection protection: m types of resource demand
        population levels: l levels maps population down to a fewer levels
    """

    # https://satran.in/b/python--dangerous-default-value-as-argument
    # https://stackoverflow.com/questions/2…

    # do not do default assignment, it remembers it on eash call
    # https://docs.python.org/3/library/typing.html
    def __init__(self, name, log_root: Optional[Log] = None):
        """Initialize the model.

        Use the data dictionary load data
        """
        # the long description of each
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)

        # https://reinout.vanrees.org/weblog/2015/06/05/logging-formatting.html
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"{__name__=}")

        self.name: str = name
        if not log.hasHandlers():
            print(f"{log=} has no handlers")

        log.debug(f"{self.name=}")
        self.data: ModelData = ModelData({}, {}, {}, {})

    def set_configure(self, config) -> Model:
        """Configure the Model.

        Uses Loaded as a dictionary and puts it into model variables
        """
        log = self.log
        self.config = config

        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        # TODO: with the new labeling, this is easy to make a loop
        self.dim: Dict[str, int] = {
            "n": len(self.config["Label"]["Resource n"].get()),
            "a": len(self.config["Label"]["Res Attribute a"].get()),
            "p": len(self.config["Label"]["Population p"].get()),
            "d": len(self.config["Label"]["Pop Detail d"].get()),
            "m": len(self.config["Label"]["Demand m"].get()),
            "l": len(self.config["Label"]["Pop Level l"].get()),
            "s": len(self.config["Label"]["Res Safety Stock s"].get()),
        }
        log.debug(f"{self.dim=}")
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
                self.config, self.filter, log_root=self.log_root,
            )
        elif type == "dict":
            # change this to the the naming of columns
            self.population = PopulationDict(
                self.config,
                log_root=self.log_root,
                index="Population p",
                columns="Pop Detail d",
            )
        else:
            raise ValueError(f"{type=} not implemented")
        return self

    def set_resource(self, type: str = None) -> Model:
        """Create resource class.

        Resource
        """
        if type == "dict":
            self.resource: Resource = ResourceDict(
                self.config, log_root=self.log_root
            )
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
        elif type == "washington":
            self.demand = DemandWA(
                self.config,
                self.population,
                self.resource,
                log_root=self.log_root,
                type=type,
            )

        else:
            log.debug("Use default yaml dictionary data")
            self.demand = DemandDict(
                self.config,
                self.population,
                self.resource,
                index="Demand m",
                columns="Resource n",
                log_root=self.log_root,
                type=type,
            )
        return self

    def set_filter(
        self, county: str = None, state: str = None, population: str = None
    ) -> Model:
        """Filter the model.

        Shrink the model to relevant population, resource
        """
        self.filter = Filter(
            log_root=self.log_root,
            county=county,
            state=state,
            population=population,
        )

        return self

    def set_economy(self, type: str = None) -> Model:
        """Create Econometric model.

        Economy creation
        """
        self.economy = Economy(self.data, log_root=self.log_root, type=type)
        return self

    def set_disease(self, type: str = None) -> Model:
        """Create Disease model.

        Disease create
        """
        self.disease = Disease(self.data, log_root=self.log_root, type=type)
        return self

    def set_activity(self, type: str = None) -> Model:
        """Create Social activity model.

        Includes social activity, restaurant usage, credit card use and other
        indicators of people out and about
        """
        self.activity = Activity(self.data, log_root=self.log_root, type=type)
        return self

    def set_behavioral(self, type: str = None) -> Model:
        """Create Behavior model.

        Behavior create
        """
        self.behavioral = Behavioral(
            self.data, log_root=self.log_root, type=type
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
