"""Define Model definition.

The model shape is configured here.
https://www.w3schools.com/python/python_classes.asp
"""
from typing import Dict, Optional
from base import Base
from util import Log
from config import Config

import logging  # noqa: F401

log = logging.getLogger(__name__)
# https://reinout.vanrees.org/weblog/2015/06/05/logging-formatting.html
log.debug(f"{__name__=}")


class Model(Base):
    """Main model for planning.

    It sets the dimensionality of the problem and also the names of all the
    elements. Each subsystem will take the dimensions and names as inputs.

    They then will create the correct tables for use by the main computation
    This model has pointers to the major elements of the model.

    Attr:
    name: the friendly string name
    labels: This is what structures the entire model with a list of labels
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
    def __init__(self, name, config: Config, log_root: Optional[Log] = None):
        """Initialize the model.

        Use the config dictionary to configure the most
        """
        # the long description of each
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        if log_root is not None:
            self.log_root = log_root
            self.log = log_root.log_class(self)
            log = self.log

        log.debug(f"{config.dict=}")

        self.name: str = name
        log.debug(f"{self.name=}")

        # https://realpython.com/python-keyerror/
        self.config: Optional[Dict] = self.config.dict.get("Config")
        log.debug(f"{self.dict=}")

        self.label: Optional[Dict] = self.raw.get("Label")
        log.debug(f"{self.label=}")

        self.description: Optional[Dict] = self.raw.get("Description")
        log.debug(f"{self.description=}")

        self.data: Optional[Dict] = self.raw.get("Data")
        log.debug(f"{self.data=}")
        # model arity
        self.label = config.model
        log.debug(f"{self.label=}")

        # the actual data
        self.data = config.data
        log.debug(f"{self.data=}")

        self.description = config.description
        log.debug(f"{self.description}")

        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        # TODO: with the new labeling, this is easy to make a loop
        self.dim: Dict[str, int] = {
            "n": len(self.label["Resource n"]),
            "a": len(self.label["Res Attribute a"]),
            "p": len(self.label["Population p"]),
            "d": len(self.label["Pop Detail d"]),
            "m": len(self.label["Protection m"]),
            "l": len(self.label["Pop Level l"]),
            "s": len(self.label["Res Safety Stock s"]),
        }
        log.debug(f"{self.dim=}")
