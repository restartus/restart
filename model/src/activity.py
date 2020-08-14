"""Activity Model.

Activity modeling
"""
from typing import Optional

import confuse  # type: ignore
import numpy as np  # type: ignore # noqa: F401
import pandas as pd  # type: ignore # noqa: F401

from base import Base
from log import Log


class Activity(Base):
    """The amount of acivity and movement.

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
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529

        super().__init__(log_root=log_root)
        # create a sublogger if a root exists in the model
        log = self.log
        # if log_root is not None:
        #     log = self.log = log_root.log_class(self)
        #     log_root.con.setLevel(logging.DEBUG)
        #     log.debug(f"in {__name__=}")
        #     log_root.con.setLevel(logging.WARNING)
        # else:
        #     log = self.log = logging.getLogger(__name__)
        # the sample code to move up the logging for a period and then turn it
        # off

        log.debug(f"not implemented {type=}")
