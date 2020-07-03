"""
MOdel definition
https://www.w3schools.com/python/python_classes.asp
"""
from typing import List, Dict, Any
from base import Base

import logging  # noqa: F401

log = logging.getLogger(__name__)
# https://reinout.vanrees.org/weblog/2015/06/05/logging-formatting.html
log.debug(f"in {__name__=}")


class Model(Base):
    """ Main model for planning
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
    def __init__(
        self, name, label: Dict[str, List[str]] = None, log_root: Any = None
    ):
        """Initialize the model
        """
        # the long description of each
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        self.log = log
        if log_root is not None:
            self.log_root = log_root
            self.log = log_root.class_log(self)

        if label is None:
            label = {
                "Resource": ["N95", "ASTM3"],
                "Res Attribute": ["Units", "Dimensions"],
                "Res Supply": ["Days"],
                "Population": [
                    "Healthcare workers",
                    "Non-heathcare employees",
                ],
                "Pop Detail": ["People"],
                "Pop Protection": [
                    "WA0",
                    "WA1",
                    "WA2",
                    "WA3",
                    "WA4",
                    "WA5",
                    "WA6",
                ],
                "Pop Level": ["Essential", "Non-essential"],
            }

        self.name: str = name
        self.label: Dict[str, List[str]] = label

        print(f"{self.name=} {self.label=}")
        log.debug(f"{self.name=} {self.label=}")
        self.log.debug(f"{self.name=} {self.label=}")

        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        self.dim: Dict[str, int] = {
            "n": len(self.label["Resource"]),
            "a": len(self.label["Res Attribute"]),
            "s": len(self.label["Res Supply"]),
            "p": len(self.label["Population"]),
            "d": len(self.label["Pop Detail"]),
            "m": len(self.label["Pop Protection"]),
            "l": len(self.label["Pop Level"]),
        }
