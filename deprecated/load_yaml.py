"""Read YAML files to get base configuration.

Here is a test.
http://zetcode.com/python/yaml/
"""
import logging
import os
from typing import Any, Dict, Iterator, List, Optional

import yaml

from load import Load
from log import Log


class LoadYAML(Load):
    """Load YAML Files.

    Model configuration from YAML files
    """

    # no variable here unless you want them the same across all instances

    def __init__(
        self,
        *paths,
        log_root: Optional[Log] = None,
        ext: List[str] = [".yaml", ".yml"],
    ):
        """Read Configuration YAML.

        Figure out how to make YAML reading work
        note that this causes the latest dictionary to overwrite prior
        entries so order matters if you have duplicates
        """
        super().__init__()
        self.root_log: Optional[Log]
        self.data: Dict = {}

        # replace the standalone logger if asked
        self.root_log = log_root
        if log_root is not None:
            log = self.log = log_root.log_class(self)
            log.debug(f"{self.log=} {log=}")
        else:
            # TODO: the scoping doesn't work, log here cannot be
            # changed by __init__
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"module {__name__=}")

        # https://gist.github.com/treyhunner/f35292e676efa0be1728
        # https://www.geeksforgeeks.org/packing-and-unpacking-arguments-in-python/
        # Unpacking works in Python 3.6+
        log.debug(f"{paths=}")
        for path in paths:
            log.debug(f"{path=}")

        self.ext = ext
        for path in paths:
            log.debug(f"{path=}")
            # note we are ignoring directories as os.walk gives us
            #  all the files
            for parent, dirs, files in os.walk(path):
                log.debug(f"{files=}")
                for file in files:
                    log.debug(f"{file=}")
                    # https://www.geeksforgeeks.org/python-os-path-splitext-method/
                    base, ext = os.path.splitext(file)
                    log.debug(f"{ext=}")
                    if ext not in self.ext:
                        log.debug(f"skipping {file=}")
                        continue
                    full_path = os.path.join(parent, file)
                    data: Optional[Dict] = self.load(full_path)
                    if data is not None:
                        self.data = {**self.data, **data}

    def load(self, filename: str) -> Optional[Dict]:
        """Load configuration.

        Load a Yaml file with one
        """
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
