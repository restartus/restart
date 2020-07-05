"""Main Routine.

Here is a test.
http://zetcode.com/python/yaml/
"""
import logging
import yaml
from typing import Optional, Dict, Iterator
from util import Log

log = logging.getLogger(__name__)
root_log = Log(None)


def main():
    """Let's get started.

    Figure out how to make YAML reading work
    """
    print('hello world')
    log.critical(f'log.critical {__name__=}')
    c: Dict = config()
    root_log.log.info(f'rootlog info hello {c=}')
    model_data: Iterator = load_model()
    for item in model_data:
        root_log.log.debug(f'{item=}')


def config(filename: Optional[str] = None) -> Optional[Dict]:
    """Load configuration.

    Load a Yaml file
    """
    if filename is None:
        filename = 'config.yaml'
    try:
        with open(filename) as f:
            # bandit says use the safe loader
            # config = yaml.load(c, Loader=yaml.FullLoader)
            config = yaml.load(f, Loader=yaml.SafeLoader)
            root_log.log.critical(f'{config=}')
            return config

    except IOError:
        root_log.log.critical('No {filename=} exists')
        return None


def load_model(filename: Optional[str] = None) -> Optional[Iterator]:
    """Load model from YAML file.

    Load from an optional file
    """
    if filename is None:
        filename = 'model.yaml'
    try:
        # https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python
        with open(filename, 'r') as f:
            # model_data = yaml.load(f, Loader=yaml.FullLoader)
            model_data = yaml.safe_load_all(f)
            root_log.log.debug(f'{model_data=}')
            for d in model_data:
                root_log.log.debug(f'{d=}')
            return model_data

    except yaml.YAMLError as err:
        root_log.log.debug(f'yaml error {err=} for {filename=}')
        return None
    except IOError:
        root_log.log.critical(f'No {filename=} exists')
        return None


if __name__ == '__main__':
    main()
