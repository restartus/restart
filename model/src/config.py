"""Read YAML files to get base configuration.

Here is a test.
http://zetcode.com/python/yaml/
"""
import logging
import yaml
from typing import Optional, Dict, Iterator, Any
from util import Log

log = logging.getLogger(__name__)


class Config:
    """Configure the model.

    Model configuration from YAML files
    """

    dict: Dict = {}

    def __init__(
        self, *files, log_root: Optional[Log] = None,
    ):
        """Let's get started.

        Figure out how to make YAML reading work
        note that this causes the latest dictionary to overwrite prior
        entries so order matters if you have duplicates
        """
        # replace the standalone logger if asked
        if log_root is not None:
            self.root_log = log_root
            self.log = log_root.log_class(self)
            log = self.log
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

    def load_all(self, filename: str) -> Optional[Iterator[Any]]:
        """Load multiple documents from a single YAML file.

        Load from an optional file
        """
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
