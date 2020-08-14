"""Loader CSV.

The loader for the CSV
"""
import os
from typing import Dict, List, Optional

import pandas as pd  # type:ignore

from load import Load
from log import Log


class LoadCSV(Load):
    """Converts Excel and CSV files into dataframe objects.

    If you give it files with a .xlsx, .xls, or .csv extension, it will read
    their data into a dataframe, and then safe the dataframe as
    a h5 file with extension .h5. If you feed this class
    a h5 file, it will simply pass through this class. This is
    done so that we can minimize the amount of times the Excel/CSV
    data must be processed - for larger files, it can be lengthy.

    Attributes:
        excel_ext: list of extensions attached to excel files
        csv_ext: list of extensions attached to csv files
        data: dictionary containing names of h5 files
    """

    def __init__(
        self,
        source: Dict = None,
        log_root: Optional[Log] = None,
        excel_ext: List[str] = [".xlsx", ".xls"],
        csv_ext: List[str] = [".csv"],
    ):
        """Initialize the Loader to read files.

        Reads the files
        """
        # logging setup
        super().__init__(log_root=log_root)
        log = self.log
        log.debug(f"{self.log=} {log=}")
        log.debug(f"module {__name__=}")

        # extensions we check for
        self.excel_ext = excel_ext
        self.csv_ext = csv_ext

        if source is None:
            raise ValueError(f"{source=} should not be None")

        try:
            if source["Root"] is None:
                raise ValueError(f"need root directory in {source=}")
        except KeyError:
            log.debug(f"{source=} invalid config")
            return None

        # read all files in the given root directory
        files = os.listdir(source["Root"])
        rootdir = source["Root"]

        self.data: Dict = source

        for fname in source:

            # skip root key
            if not fname == "Root":
                path = source[fname]
                log.debug(f"{path=}")

                # split paths into name + extension
                base, ext = os.path.splitext(path)
                fullbase = os.path.join(rootdir, base)

                try:
                    # look for h5 file in rootdir
                    if base + ".h5" in files:
                        log.debug(f"preexisting json found for {base=}")
                        self.data[fname] = base + ".h5"

                    else:
                        log.debug(f"generating h5 file for {base=}")

                        # excel to dataframe
                        if ext in self.excel_ext:
                            log.debug(f"loading {ext=} file")
                            df = pd.read_excel(fullbase + ext)

                        # csv to dataframe
                        elif ext in self.csv_ext:
                            log.debug(f"loading {ext=} file")
                            df = pd.read_csv(fullbase + ext)

                        else:
                            raise ValueError(f"{fname=} extension invalid")

                        # store dataframe and overwrite dictionary input
                        self.store_dataframe(fullbase, df)
                        self.data[fname] = base + ".h5"

                # handle alternate utf encodings
                except UnicodeDecodeError:
                    log.debug(f"loading {ext=} file with ISO-8859-1 encoding")
                    df = pd.read_csv(fullbase + ext, encoding="ISO-8859-1")
                    self.store_dataframe(fullbase, df)
                    self.data[fname] = base + ".h5"

    def store_dataframe(self, name: str, df: pd.DataFrame) -> None:
        """Serializes a dataframe in h5 format.

        Args:
            name: name of the file we want to save

        Returns:
            None
        """
        log = self.log
        name = name + ".h5"
        log.debug(f"{name=}")
        df.to_hdf(name, key="df", mode="w")

        return None
