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

    def __init__(
        self,
        log_root: Optional[Log] = None,
        config_file: str = "config.yaml",
        model_file: str = "model.yaml",
        description_file: str = 'description.yaml',
        data_file: str = "data.yaml",
    ):
        """Let's get started.

        Figure out how to make YAML reading work
        """
        # replace the standalone logger if asked
        if log_root is not None:
            self.root_log = log_root
            self.log = log_root.log_class(self)
            log = self.log
        log.debug(f"module {__name__=}")

        self.parm: Optional[Dict] = self.load(config_file)
        if self.parm is not None:
            self.parm = self.parm["Config"]
        log.debug(f"{self.parm=}")

        self.label: Optional[Dict] = self.load(model_file)
        if self.label is not None:
            self.label = self.label["Label"]
        log.debug(f"{self.label=}")

        self.description: Optional[Dict] = self.load(
            description_file)
        if self.description is not None:
            self.description = self.description["Description"]
        log.debug(f"{self.description=}")

        self.data: Optional[Dict] = self.load(model_file)
        log.debug(f"{self.data=}")

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
