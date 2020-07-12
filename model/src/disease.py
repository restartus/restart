"""Disease model.

The disease model work.
"""

# https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html
# note the noqa: and type: are space sensitive
# https://stackoverflow.com/questions/51179109/set-pyflake-and-mypy-ignore-same-line
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from model import Model
from typing import Optional

log = logging.getLogger(__name__)


class Disease(Base):
    """Resource - Manages all the resources that are used in the model.

    This creates for all r resources, the list of attributes a

    This contains
    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    # no variable here unless you want them the same across all classes
    # see https://docs.python.org/3/tutorial/classes.html
    def __init__(self, model: Model, type: Optional[str]):
        """Initialize the Disease object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()
        # create a sublogger if a root exists in the model
        global log
        self.log = log
        if model.log_root is not None:
            log = self.log = model.log_root.log_class(self)

        if type is not None:
            log.debug(f"not implemented {type=}")
