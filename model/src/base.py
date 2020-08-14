"""Base for all Classes.

Base mainly includes the description fields
"""
import logging
from typing import Dict, Optional, Tuple

import pandas as pd  # type:ignore

from log import Log


class BaseLog:
    """Logging is at the very bottom."""

    def __init__(self, log_root: Optional[Log] = None):
        """Set the Root Log."""
        # since we have no log otherwise
        self.log_root = log_root
        self.log = (
            log_root.log_class(self)
            if log_root is not None
            else logging.getLogger(__name__)
        )
        self.log.debug(f"{self=}")


class Base(BaseLog):
    """Base for all model classes.

    Base strings and description.
    """

    # do not put variable here unless you want them the same
    # across all classes see https://docs.python.org/3/tutorial/classes.html

    # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    def __init__(self, log_root: Log = None):
        """Set base varabiles.

        Mainly the descriptions
        """
        super().__init__(log_root=log_root)
        self.description: Dict = {}

    def set_description(self, name: str, description: str):
        """Set the variable description.

        The descriptions are carried in each class so they are self documenting
        May change this to centralized at some point.
        Gets rid of the equal sign if it is there from a f string
        Also only uses the last member name
        """
        # we can't use a higher level logger
        log: logging.Logger = logging.getLogger(__name__)

        # https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string/58451182#58451182
        # Using Python 3.8 f strings
        # you must use double quotes inside single quotes for strings
        log.debug(f"{object=}")
        # this doesn't work, we need the real object's name so has to happen in
        # caller
        # name = f'{object=}'.split('=')[0]
        # log.debug(f'set self.description[{name}]')
        # https://stackoverflow.com/questions/521502/how-to-get-the-concrete-class-name-as-a-string
        # pdb.set_trace()
        class_name = self.__class__.__name__
        # https://stackoverflow.com/questions/599953/how-to-remove-the-left-part-of-a-string
        # clean up the name so you only get the basename after the period
        # https://www.tutorialspoint.com/How-to-get-the-last-element-of-a-list-in-Python
        name = name.split("=")[0].split(".")[-1]
        model_name = class_name + "." + name
        log.debug(f"{model_name=} {name=}")
        # log.debug(f'set model.description[{model_name}]')
        self.description[name] = description

        # method chaining
        return self

    def __iter__(self):
        """Iterate over all Pandas DataFrames.

        Uses a list of all frames
        """
        self.df_list = [
            k for k, v in vars(self).items() if isinstance(v, pd.DataFrame)
        ]
        self.df_len = len(self.df_list)
        self.df_index = 0
        return self

    def __next__(self) -> Tuple[str, pd.DataFrame]:
        """Next Pandas DataFrame.

        Iterates through the list of dataframes
        """
        if self.df_index >= self.df_len:
            raise StopIteration
        key = self.df_list[self.df_index]
        value = vars(self)[key]
        self.df_index += 1
        return key, value
