"""Base class for Loader.

BAse class
"""
import logging
from util import Log
from typing import Optional, Dict

# TODO: the scoping doesn't work, log here cannot be
# changed by __init__
log: logging.Logger = logging.getLogger(__name__)


class Load():
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
        self.root_log: Optional[Log]
        self.data: Dict = {}

        global log
        # replace the standalone logger if asked
        if log_root is not None:
            self.root_log = log_root
            log = self.log = log_root.log_class(self)
            log.debug(f"{self.log=} {log=}")

        log.debug(f"module {__name__=}")
