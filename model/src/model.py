"""Define Model definition.

The model shape is configured here.
https://www.w3schools.com/python/python_classes.asp
"""
from typing import Dict, Optional, Tuple, List
from base import Base
from util import Log
from loader.load import Load
import numpy as np  # type:ignore
import pandas as pd  # type:ignore

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
    def __init__(self, name, loaded: Load, log_root: Optional[Log] = None):
        """Initialize the model.

        Use the data dictionary load data
        """
        # the long description of each
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()
        global log
        self.log: logging.Logger = log
        self.data: Dict = {}
        self.label: Dict = {}
        if log_root is not None:
            self.log_root = log_root
            self.log = log_root.log_class(self)
            log = self.log

        log.debug(f"{loaded.data=}")

        self.name: str = name
        log.debug(f"{self.name=}")

        # https://realpython.com/python-keyerror/
        cfg: Optional[Dict] = loaded.data.get("Config")
        if cfg is not None:
            self.config = cfg
        log.debug(f"{self.config=}")

        description: Optional[Dict] = loaded.data.get("Description")
        if description is not None:
            self.description = description
        log.debug(f"{self.description=}")

        data: Optional[Dict] = loaded.data.get("Data")
        log.debug(f"{data=}")
        if data is not None:
            self.data = data
        log.debug(f"{self.data=}")

        label: Optional[Dict] = loaded.data.get("Label")
        if label is None:
            log.warning(f"No label in {loaded.data=}")
            return
        self.label = label

        log.debug(f"{self.label=}")
        # These are just as convenience functions for dimensions
        # and for type checking this is ugly should make it
        # for look for assign because we are just mapping label
        # TODO: with the new labeling, this is easy to make a loop
        self.dim: Dict[str, int] = {
            "n": len(self.label["Resource n"]),
            "a": len(self.label["Res Attribute a"]),
            "p": len(self.label["Population p"]),
            "d": len(self.label["Pop Detail d"]),
            "m": len(self.label["Pop Protection m"]),
            "l": len(self.label["Pop Level l"]),
            "s": len(self.label["Res Safety Stock s"]),
        }
        log.debug(f"{self.dim=}")

    # sets the frame properly but does need to understand the model
    # so goes into the model method
    def dataframe(
        self, arr: np.ndarray, index: str = None, columns: str = None,
    ) -> pd.DataFrame:
        """Set the dataframe up.

        Using the model data Dictionary and labels
        """
        log.debug(f"{arr=}")
        df = pd.DataFrame(
            arr, index=self.label[index], columns=self.label[columns],
        )
        df.index.name = index
        df.columns.name = columns
        log.debug(f"{df=}")
        return df

    # https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints
    # https://www.datacamp.com/community/tutorials/python-iterator-tutorial
    # https://towardsdatascience.com/how-to-loop-through-your-own-objects-in-python-1609c81e11ff
    # So we want the iterable to be the Base Class
    # The iterator is Model which can return all the Base classes
    # https://thispointer.com/python-how-to-make-a-class-iterable-create-iterator-class-for-it/
    def __iter__(self):
        """Iterate through the model getting only Base objects."""
        self.base_list: List = [
            k for k, v in vars(self).items() if isinstance(v, Base)
        ]
        log.debug(f"{self.base_list=}")
        self.base_len: int = len(self.base_list)
        self.base_index: int = 0
        return self

    def __next__(self) -> Tuple[str, Base]:
        """Next Base."""
        if self.base_index >= self.base_len:
            raise StopIteration
        log.debug(f"{self.base_index=}")
        key = self.base_list[self.base_index]
        value = vars(self)[key]
        log.debug(f"{key=} {value=}")
        self.base_index += 1
        return key, value
