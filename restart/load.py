"""Base class for Loader.

Base class
"""
from typing import Dict, Optional

from base import BaseLog
from log import Log


class Load(BaseLog):
    """Base Load YAML Files.

    Base configuration from YAML files
    """

    # no variable unless they are the same across all instances

    def __init__(
        self,
        *paths,
        log_root: Optional[Log] = None,
    ):
        """Initialize Loader Base Class.

        Base class just sets a logger
        """
        super().__init__(log_root=log_root)
        log = self.log
        self.data: Dict = {}

        # replace the standalone logger if asked
        log = self.log

        log.debug(f"{self.log=} {log=}")
        log.debug(f"module {__name__=}")
