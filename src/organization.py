"""Organization Model.

Organization modeling
"""
from typing import Optional

import confuse  # type: ignore

from base import Base
from data import Data
from log import Log


class Organization(Base):
    """The amount of use by Organization.

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Organization object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        # pass the logger down
        super().__init__(log_root=log_root)
        self.config = config
        # create a sublogger if a root exists in the model
        # self.log_root = log_root
        # log = self.log = (
        #     log_root.log_class(self)
        #     if log_root is not None
        #     else logging.getLogger(__name__)
        # )
        # the sample code to move up the logging for a period and then turn it
        # off
        log = self.log
        log.debug(f"in {__name__=}")

        self.organization_oO_tr: Optional[Data] = None
        self.org_demand_per_unit_map_od_um: Optional[Data] = None
        self.org_to_orgsum1_per_unit_map_oo1_us: Optional[Data] = None
