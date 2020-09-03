"""Output module.

Automatically generates config files
"""
from typing import Callable, Dict

import confuse  # type: ignore
import yaml

from base import Base
from log import Log


class Output(Base):
    """Creates an output object.

    Supply a callback that provides each model element in turn since we
    we cannot pass it. For while mutual import fails so instead we need
    a callback so that output and run through all the elements of model.
    http://effbot.org/pyfaq/how-can-i-have-modules-that-mutually-import-each-other.htm
    """

    def __init__(
        self,
        get_element: Callable,
        config: confuse.Configuration,
        log_root: Log = None,
        out: str = None,
        csv: str = None,
    ):
        """Do the initializing.

        Generate the config files
        """
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        self.config = config
        self.out = out
        self.csv = csv

        self.generate_config(get_element)
        self.write_csv()

    def generate_config(self, get_element: Callable):
        """Generate a new config yaml."""
        log = self.log
        new_config: Dict = {}

        for section in ["Parameter", "Dimension", "Paths", "Model"]:
            new_config[section] = self.config[section].get()
        log.debug(f"Wrote all config data into {new_config=}")

        # get the in memory data read from csv's and elsewhere or computed
        # note you cannot pass the model over so you need to do this as a call
        # back but the code looks like
        for key, value in get_element():
            # we have more in memory objects than in the Model
            # so check for existance. For instance filtering is in memory only
            if key in new_config["Model"]:
                new_config["Model"][key]["array"] = value.array

        self.write_config(new_config)

    def write_config(self, config: Dict):
        """Writes config dict to yaml file."""
        if self.out is not None:
            with open(self.out, "w") as yamlfile:
                yaml.dump(config, yamlfile)

    def write_csv(self):
        """Writes to a CSV file."""
        if self.csv is not None:
            df = self.demand.total_demand_pn_df.copy()
            # insert population into the dataframe
            pop = list(self.pop.detail_pd_df["Size"])
            df.insert(loc=0, column="Size", value=pop)
            df.to_csv(self.csv)
