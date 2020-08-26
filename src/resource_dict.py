"""The Resource Model.

Reads from dictionary for defaults
"""

import confuse  # type: ignore

from data import Data
from log import Log
from resourcemodel import Resource


class ResourceDict(Resource):
    """ResourceDict - pulls resources from the default config yaml files.

    This can be a default for testing
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
    ):
        """Initialize the resources.

        Reads from the default config yaml files
        """
        # to pick up the description
        super().__init__(config, log_root=log_root)
        log = self.log
        log.debug(f"in {__name__}")

        self.resource_nN_ur = Data("resource_nN_ur", config, log_root=log_root)
        log.debug(f"{self.resource_nN_ur=}")

        self.res_by_popsum1_cost_per_unit_p1n_us = Data(
            "res_by_popsum1_cost_per_unit_p1n_us", config, log_root=log_root
        )
        log.debug(f"{self.res_by_popsum1_cost_per_unit_p1n_us=}")
