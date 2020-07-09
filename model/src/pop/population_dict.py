"""Population Data Read.

Read in the population from the model dictionary
"""
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore
# https://www.python.org/dev/peps/pep-0420/
from base import Base
from model import Model
from typing import Optional

log = logging.getLogger(__name__)


class PopulationDict(Base):
    """Population Data Readers.

    Reads the population data. The default is to read from the model.data
    """

    # https://stackoverflow.com/questions/35328286/how-to-use-numpy-in-optional-typing
    data_arr: Optional[np.ndarray] = None
    data_df: Optional[pd.DataFrame] = None

    def __init__(
        self,
        model: Model,
        source=None,  # TODO: Figure out typing for this
        index: Optional[str] = None,
        columns: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__()

        global log
        # create a sublogger if a root exists in the model
        self.model = model
        if model.log_root is not None:
            log = self.log = model.log_root.log_class(self)
        # the sample code to move up the logging for a period and then turn it
        # off
        self.model.log_root.con.setLevel(logging.DEBUG)
        log.debug(f"in {__name__=}")
        self.model.log_root.con.setLevel(logging.WARNING)

        log.debug(f"{type(self.data_arr)=}")

        if source is not None:
            self.data_arr = np.array(source['Size'])  # TODO: Don't hardcode
        if index is not None and columns is not None:
            self.data_df = pd.DataFrame(
                self.data_arr, index=index, columns=columns,
            )
