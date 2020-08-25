"""Demand Model.

Demand modeling
"""
from typing import Dict, Optional

import confuse  # type: ignore

from base import Base
from data import Data
from log import Log
from population import Population
from resourcemodel import Resource


class Demand(Base):
    """Calculate consumption based on Population and Resource.

    Take in Pop and and Res and into model.data["Pop Res Demand pn"]
    Some parameters are to use:
    - Washington estimate
    - Mitre burn rates
    - Johns Hopkins burn rates
    - CDPH estimates
    - Ensemble

    If pop and res aren't set by default take the existing Population and
    resource already in the model.data

    With dimensions ["Population p"]["Resource n"]

    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        config: confuse.Configuration,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"In {__name__}")

        # Make sure to instantiate each of these for inheritance purposes
        self.demand_per_unit_map_dn_um: Optional[Data] = None
        self.demand_by_pop_per_person_pn_uc: Optional[Data] = None
        self.demand_by_pop_total_pn_tc: Optional[Data] = None
        self.demand_by_pop_total_cost_pn_tc: Optional[Data] = None

        self.demand_by_popsum_ps_us: Optional[Dict] = None

        self.demand_by_popsum1_per_person_p1n_uc: Optional[Data] = None
        self.demand_by_popsum1_total_p1n_tc: Optional[Data] = None
        self.demand_by_popsum1_total_cost_p1n_tc: Optional[Data] = None
