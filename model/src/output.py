"""Output module.

Automatically generates config files
"""
import logging
import confuse  # type: ignore
import yaml
from typing import Dict
from base import Base
from population import Population
from resourcemodel import Resource
from demand import Demand
from util import Log


class Output(Base):
    """Creates an output object."""

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population,
        resource: Resource,
        demand: Demand,
        log_root: Log = None,
        type: str = None,
    ):
        """Do the initializing.

        Generate the config files
        """
        super().__init__(log_root=log_root)
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"In {__name__}")

        self.config = config
        self.pop = pop
        self.resource = resource
        self.demand = demand
        self.type = type

        self.generate_config()

    def generate_config(self):
        """Generate a new config yaml."""
        new_config = {}

        # copy over the fields that don't change
        new_config["Config"] = self.config["Config"].get()
        new_config["Description"] = self.config["Description"].get()
        new_config["Paths"] = self.config["Paths"].get()

        # get the new data
        new_config["Data"] = {}
        new_config["Data"]["Population p"] = {}
        new_config["Data"]["Population p"]["Pop Detail Data pd"] = {}
        new_config["Data"]["Population p"]["Pop Detail Data pd"][
            "Size"
        ] = list(self.pop.detail_pd_df["Size"])
        new_config["Data"]["Protection pm"] = self.pop.level_pm_arr.tolist()
        new_config["Data"]["Pop to Level pl"] = self.demand.level_pl_arr
        new_config["Data"]["Demand m"] = {}
        new_config["Data"]["Demand m"][
            "Level to Resource mn"
        ] = self.demand.level_to_res_mn_arr.tolist()
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
        if self.type is not None:
            with open(self.type, "w") as yamlfile:
                yaml.dump(config, yamlfile)
