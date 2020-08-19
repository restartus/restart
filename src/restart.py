"""Compose the model without a CLI."""
from typing import Optional

from log import Log
from model import Model
from util import set_config


class NoteCompose:
    """Bootstrap a model object in a notebook environment."""

    def __init__(
        self,
        population: str = "dict",
        organization: Optional[str] = None,
        csv: Optional[str] = None,
        county: Optional[str] = None,
        state: Optional[str] = None,
        subpop: Optional[str] = None,
        configdir: str = ".",
        output: Optional[str] = None,
        resource: str = "dict",
        demand: str = "dict",
        economy: str = "ml",
        behavioral: str = "ensemble",
        activity: str = "ensemble",
        disease: str = "imhe",
    ):
        """Initialize a model object."""
        # set up the logging
        name = "model"
        self.log_root = Log(name)
        self.log = log = self.log_root.log
        log.propagate = False
        log.debug(f"{__name__=}")

        # set up the config
        self.config = set_config(configdir)

        self.model = (
            Model(name, log_root=self.log_root)
            .set_configure(self.config)
            .set_filter(county=county, state=state, subpop=subpop)
            .set_population(type=population)
            .set_organization(type=organization)
            .set_resource(type=resource)
            .set_demand(type=demand)
            .set_economy(type=economy)
            .set_disease(type=disease)
            .set_activity(type=activity)
            .set_behavioral(type=behavioral)
            .set_output(out=output, csv=csv)
        )
