"""Organization Model using Dictionary Input.

Organization modeling
"""
import confuse  # type: ignore

from data import Data
from log import Log
from organization import Organization


class OrganizationDict(Organization):
    """Stub for org from reading a dictionary."""

    def __init__(self, config: confuse.Configuration, log_root: Log = None):
        """Set some variables."""
        super().__init__(config, log_root=log_root)
        log = self.log

        self.organization_oO_tr = Data(
            "organization_oO_tr", config, log_root=log_root
        )

        log.debug(f"{self.organization_oO_tr=}")
