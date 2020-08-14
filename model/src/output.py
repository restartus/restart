"""Output module.

Automatically generates config files
"""
from typing import Dict

import confuse  # type: ignore
import numpy as np  # type: ignore
import yaml

from base import Base
from demand import Demand
from log import Log
from population import Population
from resourcemodel import Resource


class Output(Base):
    """Creates an output object."""

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population,
        resource: Resource,
        demand: Demand,
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
        self.pop = pop
        self.resource = resource
        self.demand = demand
        self.out = out
        self.csv = csv

        self.generate_config()
        self.write_csv()

    def generate_config(self):
        """Generate a new config yaml."""
        new_config = {}

        # copy over the fields that don't change
        new_config["Config"] = dict(self.config["Config"].get())
        new_config["Description"] = dict(self.config["Description"].get())
        for key in new_config["Description"].keys():
            new_config["Description"][key] = dict(
                new_config["Description"][key]
            )
        new_config["Paths"] = dict(self.config["Paths"].get())

        # get the new data
        new_config["Data"] = {}
        new_config["Data"]["Population p"] = {}
        new_config["Data"]["Population p"]["Pop Detail Data pd"] = {}
        new_config["Data"]["Population p"]["Pop Detail Data pd"][
            "Size"
        ] = list(self.pop.detail_pd_df["Size"])
        new_config["Data"]["Population p"][
            "Protection pm"
        ] = self.pop.level_pm_arr.tolist()
        new_config["Data"]["Population p"]["Pop to Level pl"] = np.array(
            self.demand.level_pl_arr
        ).tolist()
        new_config["Data"]["Demand m"] = {}
        new_config["Data"]["Demand m"]["Level to Resource mn"] = np.array(
            self.demand.level_to_res_mn_df
        ).tolist()
        new_config["Data"]["Resource n"] = {}
        new_config["Data"]["Resource n"][
            "Res Attr Data na"
        ] = self.resource.attr_na_arr
        new_config["Data"]["Resource n"][
            "Pop Level Res Cost ln"
        ] = self.resource.cost_ln_arr
        new_config["Data"]["Resource n"][
            "Res Inventory Initial ln"
        ] = self.resource.inv_initial_ln_arr
        new_config["Data"]["Resource n"][
            "Res Inventory EOC ln"
        ] = self.resource.inv_eoc_ln_arr
        new_config["Data"]["Resource n"][
            "Res Inventory Min ln"
        ] = self.resource.inv_min_rln_arr
        new_config["Data"]["Resource n"][
            "Res Inventory Min in Periods ln"
        ] = self.resource.inv_min_in_periods_arr

        # get the new labels
        new_config["Label"] = {}
        new_config["Label"]["Resource n"] = list(
            self.demand.demand_pn_df.columns
        )
        new_config["Label"]["Population p"] = list(self.pop.detail_pd_df.index)
        new_config["Label"]["Pop Detail d"] = list(
            self.pop.detail_pd_df.columns
        )
        new_config["Label"]["Pop Level l"] = list(
            self.demand.level_pl_df.columns
        )
        new_config["Label"]["Demand m"] = list(
            self.demand.level_to_res_mn_df.index
        )
        new_config["Label"]["Res Attribute a"] = list(
            self.resource.attr_na_df.columns
        )
        # TODO: this one isn't set by any classes so pulls from old config
        new_config["Label"]["Res Safety Stock s"] = self.config["Label"][
            "Res Safety Stock s"
        ].get()

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
