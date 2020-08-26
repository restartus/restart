"""Read YAML files to get base configuration.

Here is a test.
http://zetcode.com/python/yaml/
"""
import logging
from typing import Any, Dict, Iterator, Optional

import yaml

from log import Log


class Config:
    """Configure the model.

    Model configuration from YAML files
    """

    # no variables here unless you want them same across all instances
    def __init__(
        self,
        *files,
        log_root: Optional[Log] = None,
    ):
        """Read Configuration YAML.

        Figure out how to make YAML reading work
        note that this causes the latest dictionary to overwrite prior
        entries so order matters if you have duplicates
        """
        self.dict: Dict = {}
        # replace the standalone logger if asked
        if log_root is not None:
            self.root_log = log_root
            log = log_root.log_class(self)
            log.debug(f"{log=} {log=}")
        else:
            # TODO: the scoping doesn't work, log here cannot be
            # changed by __init__
            log = logging.getLogger(__name__)
        self.log = log

        log.debug(f"module {__name__=}")

        # https://gist.github.com/treyhunner/f35292e676efa0be1728
        # https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/
        # Unpacking works in Python 3.6+
        for file in files:
            dict: Optional[Dict] = self.load(file)
            if dict is not None:
                # TODO: the second arg wants Mapping, got Dict
                self.dict = {**self.dict, **dict}
        log.debug(f"{self.dict=}")

    def load(self, filename: str) -> Optional[Dict]:
        """Load configuration.

        Load a Yaml file with one
        """
        # TODO: not clear why this is not true
        # https://www.flake8rules.com/rules/F823.html
        log = self.log
        log.debug(f"{filename=}")
        try:
            with open(filename, "r") as f:
                # bandit says use the safe loader
                # config = yaml.load(c, Loader=yaml.FullLoader)
                y = yaml.load(f, Loader=yaml.SafeLoader)
                log.debug(f"{y=}")
                return y

        except IOError:
            log.error("No {filename=} exists")
            return None

        # method chaining
        return self

    def load_all(self, filename: str) -> Optional[Iterator[Any]]:
        """Load multiple documents from a single YAML file.

        Load from an optional file
        """
        log = self.log
        try:
            # https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
            with open(filename, "r") as f:
                # model_data = yaml.load(f, Loader=yaml.FullLoader)
                y = yaml.safe_load_all(f)
                log.debug(f"{y=}")
                for item in y:
                    log.debug(f"{item=}")
                return y

        except yaml.YAMLError as err:
            log.error(f"yaml error {err=} for {filename=}")
            return None
        except IOError:
            log.error(f"No {filename=} exists")
            return None
