"""Define Model definition.

The model shape is configured here.
And this uses chained methods as decorators
https://www.w3schools.com/python/python_classes.asp
"""
# https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel
# this allows Model to refer to itself
from __future__ import annotations

from typing import Dict, Optional, Tuple, List
from base import Base
from util import Log
from loader.load import Load

# import numpy as np  # type:ignore
# import pandas as pd  # type:ignore
# from population import Population
from population import Population
from pop.population_dict import PopulationDict
from pop.population_oes import PopulationOES
from resourcemodel import Resource
from consumption import Consumption
from cons.consumption_wa import ConsumptionWA
from economy import Economy
from disease import Disease
from activity import Activity
from behavioral import Behavioral
from modeldata import ModelData
from filtermodel import Filter

import logging  # noqa: F401


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
        inventory: s stockpile units
    population: p labels defines the populations
        population Details: d details about each population
        protection protection: m types of resource consumption
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

    def set_configure(self, loaded: Load) -> Model:
        """Configure the Model.

        Uses Loaded as a dictionary and puts it into model variables
        """
        log = self.log
        log.debug(f"{loaded.data=}")

        # https://realpython.com/python-keyerror/
        cfg: Optional[Dict] = loaded.data.get("Config")
        if cfg is None:
            log.warning(f"no config in {loaded.data=}")
        self.config = cfg
        log.debug(f"{self.config=}")

        description: Optional[Dict] = loaded.data.get("Description")
        if description is None:
            raise ValueError(f"no description in {loaded.data=}")
        self.data.description = description
        log.debug(f"{self.description=}")

        data: Optional[Dict] = loaded.data.get("Data")
        if data is None:
            raise ValueError(f"no data in {loaded.data=}")
        self.data.value = data
        log.debug(f"{self.data=}")

        label: Optional[Dict] = loaded.data.get("Label")
        if label is None:
            raise ValueError(f"No label in {loaded.data=}")
        self.data.label = label
        log.debug(f"{self.data.label=}")
        self.label = label
        log.debug(f"{self.label=}")

        datapaths: Optional[Dict] = loaded.data.get("Filepaths")
        if datapaths is not None:
            self.data.datapaths = datapaths
        log.debug(f"{self.data.datapaths=}")

        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        # TODO: with the new labeling, this is easy to make a loop
        self.dim: Dict[str, int] = {
            "n": len(self.data.label["Resource n"]),
            "a": len(self.data.label["Res Attribute a"]),
            "p": len(self.data.label["Population p"]),
            "d": len(self.data.label["Pop Detail d"]),
            "m": len(self.data.label["Consumption m"]),
            "l": len(self.data.label["Pop Level l"]),
            "s": len(self.data.label["Res Safety Stock s"]),
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
                self.data,
                # TODO: this belongs in filter
                {'County': None, 'State': 'California'},
                log_root=self.log_root,
            )
        elif type == "dict":
            # change this to the the naming of columns
            self.population = PopulationDict(
                data=self.data,
                label=self.data.label,
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
        self.resource = Resource(self.data, log_root=self.log_root, type=type)
        return self

    def set_consumption(self, type: str = None) -> Model:
        """Set consumption.

        Consumption by population levels l
        """
        log = self.log

        self.consumption: Consumption
        if type == "Mitre":
            log.debug("Use Mitre consumption")
            raise ValueError("{type=} not implemented")
        elif type == "Johns Hopkins":
            log.debug("Use JHU burn rate model")
            raise ValueError("{type=} not implemented")
        else:
            log.debug("For anything else use Washington data")
            self.consumption = ConsumptionWA(
                    self.data,
                    self.population,
                    self.resource,
                    log_root=self.log_root,
                    type=type)
        return self

    def set_filter(self, type: str = None) -> Model:
        """Filter the model.

        Shrink the model to relevant population, resource
        """
        self.filter = Filter(self.data, log_root=self.log_root, type=type)
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
