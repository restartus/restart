"""Financial Data Read.

Read in the financial from the model dictionary
"""

import confuse  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from data import Data
from financial import Financial
from log import Log


class FinancialDict(Financial):
    """Financial Data Readers.

    Reads the financial data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Log = None,
        type: str = None,
    ):
        """Initialize the financial object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        # get financial data
        # Using the new Lucas data class
        self.financial_fF_pr = Data(
            "financial_fF_pr",
            config,
            log_root=log_root,
        )
        log.debug(f"{self.financial_fF_pr.df=}")
