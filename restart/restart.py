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
        inventory: str = "dict",
        demand: str = "dict",
        financial: str = "dict",
        mobility: str = "ensemble",
        epi: str = "imhe",
    ):
        """Initialize a model object."""
        # set up all attributes
        for i in locals().items():
            if i[0] != "self":
                setattr(self, i[0], i[1])

        # set the logging
        self.name = "model"
        self.log_root = Log(self.name)
        self.log = log = self.log_root.log
        log.propagate = False
        log.debug(f"{__name__=}")

        # set up the config
        self.config = set_config(configdir)
        self.set_model()

    def set_model(self, **kwargs):
        """Bootstrap the model."""
        # override defaults with keywords
        for k, v in kwargs.items():
            setattr(self, k, v)
        # build the model
        self.model = (
            Model(self.name, log_root=self.log_root)
            .set_configure(self.config)
            .set_filter(
                county=self.county, state=self.state, subpop=self.subpop
            )
            .set_population(type=self.population)
            .set_organization(type=self.organization)
            .set_resource(type=self.resource)
            .set_inventory(type=self.inventory)
            .set_demand(type=self.demand)
            .set_financial(type=self.financial)
            .set_epi(type=self.epi)
            .set_mobility(type=self.mobility)
            .set_output(out=self.output, csv=self.csv)
        )
