"""Epi Data Read.

Read in the epi from the model dictionary
"""
import os
from typing import Dict, List, Optional, Tuple

import confuse  # type: ignore
import h5py  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore # noqa: F401

from .data import Data  # type: ignore
from .epi import Epi  # type: ignore
from .load_csv import LoadCSV  # type: ignore
from .log import Log  # type: ignore
from .util import load_dataframe  # type: ignore


class EpiTable(Epi):
    """Epi Data Readers.

    Reads the epi data. The default is to read from the model.data
    """

    def __init__(
        self,
        config: confuse.Configuration,
        log_root: Optional[Log] = None,
        type: str = None,
    ):
        """Initialize the epi object.

        This uses the Frame object and populates it with default data unless
        you override it
        """
        # the base class handles log management
        super().__init__(config, log_root=log_root)
        # convenience name for log
        log = self.log

        if config is None:
            raise ValueError(f"{config=} is null")

        arr: np.ndarray = self.load_and_slice(config)

        # get epi data
        # Using the new Lucas data class
        self.epi_eE_pr = Data(
            "epi_eE_pr",
            config,
            log_root=self.log_root,
            e_index=["COVID-19"],
            E_index=["Cases", "Hospitalizations", "Deaths"],
            array=arr,
        )

        log.debug(f"{self.epi_eE_pr.df=}")

    def load_and_slice(self, config: confuse.Configuration) -> np.ndarray:
        """Builds array of targets for the specified parameters.

        Loads data and indices of cube of Reich Lab collected forecasts,
        slices cube based on parameters, and returns target array (arr).

        Targets include number of new cases during week ending on specified
        date, number of new deaths during week ending on specified date,
        and number of new hospitalizations on day of specified date. Targets
        pertain to COVID-19 only (for now).

        An entry in the target array with a value of -1 indicates that
        that particular target for the specified parameters was not included
        in the Reich Lab collected forecasts.
        """

        def get_state(fips: int) -> (int):
            strfips: str = str(fips)
            if len(strfips) == 4:
                strfips = "0" + strfips
            return int(strfips[:2])

        def get_state_county(fips: int) -> (Tuple[int, int]):
            fips_str: str = str(fips)
            # check if loc is a state
            if len(fips_str) <= 2:
                return fips, 0
            # loc is a county
            state: int = get_state(fips)
            s: slice = slice(start=len(str(state)), stop=len(fips_str))
            county: int = int(fips_str[s])
            return state, county

        # set parameters for now, will take as input soon
        fips: int = 53  # WA state fips
        date: pd.Timestamp = pd.to_datetime("2020-09-05")
        state: Optional[int] = None
        county: Optional[int] = None
        state, county = get_state_county(fips)
        quantile: float = 0.5
        model: str = "IHME-CurveFit"

        source: Dict[str, str] = config["Reich"].get()

        arr: np.ndarray = None

        # read in data cube and corresponding index labels
        with h5py.File(
            os.path.join(source["Root"], source["CUBE"]), "r"
        ) as cube:
            indexdf: pd.DataFrame = pd.read_csv(
                os.path.join(source["Root"], source["INDEX"]), index_col=0
            )

            shape: Tuple[int, int, int, int, int, int] = cube[
                "zipped_reichcube"
            ].shape

            errormsg = "Dimensions of datacube do not match indices."
            assert len(shape) == len(indexdf.columns), errormsg  # nosec

            # prune indices of nans and compute index values from parameters
            date_indices: List[pd.Timestamp] = list(
                pd.to_datetime(indexdf["date_index"][: shape[0]])
            )
            state_indices: List[int] = list(
                indexdf["state_index"][: shape[1]].astype(int)
            )
            county_indices: List[int] = list(
                indexdf["county_index"][: shape[2]].astype(int)
            )
            quantile_indices: List[float] = list(
                indexdf["quantile_index"][: shape[3]]
            )
            model_indices: List[str] = list(indexdf["model_index"][: shape[4]])
            d: int = date_indices.index(date)
            s: int = state_indices.index(state)
            c: int = county_indices.index(county)
            q: int = quantile_indices.index(quantile)
            m: int = model_indices.index(model)

            # slice cube with indices to obtain array of targets
            # ":" as last index is because we want all three targets
            arr = cube["zipped_reichcube"][d, s, c, q, m, :]

            # reverse sparse rep and set proper shape
            arr[arr == 0] = -2
            arr[arr == -1] = 0
            arr[arr == -2] = -1
            arr = arr.reshape((1, shape[5]))

        return arr
