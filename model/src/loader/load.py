"""Base class for Loader.

BAse class
"""
import logging
from typing import Dict, Optional

from util import Log


class Load:
    """Base Load YAML Files.

    Base configuration from YAML files
    """

    # no variable unless they are the same across all instances

    def __init__(
        self, *paths, log_root: Optional[Log] = None,
    ):
        """Initialize Loader Base Class.

        Base class just sets a logger
        """
        super().__init__()
        self.data: Dict = {}

        # replace the standalone logger if asked
        self.root_log = log_root
        if log_root is not None:
            log = self.log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log

        log.debug(f"{self.log=} {log=}")
        log.debug(f"module {__name__=}")
