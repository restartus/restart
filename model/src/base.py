"""hello
"""
from typing import Dict, Any
from util import set_logger
import pdb  # noqa: F401

import logging

log = set_logger(__name__, level=logging.DEBUG)
log.debug(f"{__name__=}")


class Base:
    """Base for all model classes
    """

    # https://stackoverflow.com/questions/9056957/correct-way-to-define-class-variables-in-python
    def __init__(self):
        """init
        """
        #         print("in init")
        log.debug("run base")
        log.debug(f"{self=}")
        self.description: Dict[str, str] = {}

    def set_description(self, model: Any, name: str, description: str):
        """Set the variable description
        """
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
        name = name.split(".")[-1]
        model_name = class_name + "." + name
        log.debug(f"{model_name=} {name=}")
        # log.debug(f'set model.description[{model_name}]')
        model.description[model_name] = self.description[name] = description
