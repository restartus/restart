"""Main Routine.

Here is a test.
http://zetcode.com/python/yaml/
"""
import logging
from typing import Dict, Generator, Iterator, Optional

import yaml
from log import Log

old_log = logging.getLogger(__name__)
root_log = Log(None)
log = root_log.log


def main():
    """Let's get started.

    Figure out how to make YAML reading work
    """
    log.debug("hello world")
    log.critical(f"log.critical {__name__=}")
    c: Dict = config()
    log.info(f"config returned {c=}")
    model_data: Generator = load_model()
    log.debug(f"returned {model_data=}")

    # for key, value in model_data.items():
    for key, value in model_data:
        log.critical(f"{key=} {value=}")
        log.critical(f"{model_data[key]=}")


def config(filename: Optional[str] = None) -> Optional[Dict]:
    """Load configuration.

    Load a Yaml file
    """
    if filename is None:
        filename = "config.yaml"
    try:
        with open(filename) as f:
            # bandit says use the safe loader
            # config = yaml.load(c, Loader=yaml.FullLoader)
            config = yaml.load(f, Loader=yaml.SafeLoader)
            root_log.log.critical(f"{config=}")
            return config

    except IOError:
        root_log.log.critical("No {filename=} exists")
        return None


def load_model(filename: Optional[str] = None) -> Optional[Iterator]:
    """Load model from YAML file.

    Load from an optional file
    """
    if filename is None:
        filename = "model.yaml"
    try:
        # https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
        log.debug(f"opening {filename=}")
        with open(filename, "r") as f:
            # model_data = yaml.load(f, Loader=yaml.FullLoader)
            model_data: Iterator = yaml.safe_load_all(f)
            log.debug(f"{model_data=}")
            for d in model_data:
                log.debug(f"{d=}")
            # log.debug(f'{model_data[0]=}')  # type: ignore
            return model_data

    except yaml.YAMLError as err:
        log.debug(f"yaml error {err=} for {filename=}")
        return None
    except IOError:
        log.critical(f"No {filename=} exists")
        return None


if __name__ == "__main__":
    main()
