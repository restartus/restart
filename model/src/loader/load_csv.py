"""Loader CSV.

The loader for the CSV
"""
import logging
import os
import pandas as pd  # type:ignore
from loader.load import Load
from util import Log
from typing import List, Optional, Dict

log: logging.Logger = logging.getLogger(__name__)


class LoadCSV(Load):
    """Converts Excel and CSV files into dataframe objects.

    If you give
    it files with a .xlsx, .xls, or .csv extension, it will read
    their data into a dataframe, and then safe the dataframe as
    a pickle-file with the extension .p. If you feed this class
    a pickle-file, it will simply pass through this class. This is
    done so that we can minimize the amount of times the Excel/CSV
    data must be processed - for larger files, it can be lengthy.

    Attributes:
        splitpaths: List of tuples with format (path/to/file, extension)
        p_list: A list that becomes populated with the names of
                    pickle-files containing the input-data in dataframe form.
    """
    def __init__(self,
                 source: Dict = None,
                 log_root: Optional[Log] = None,
                 excel_ext: List[str] = ['.xlsx', '.xls'],
                 csv_ext: List[str] = ['.csv']):
        """Initialize the Loader to read files.

        Reads the files
        """
        # logging setup
        super().__init__()
        self.root_log: Optional[Log]
        global log

        if log_root is not None:
            self.root_log = log_root
            log = self.log = log_root.log_class(self)
            log.debug(f"{self.log=} {log=}")

        log.debug(f"module {__name__=}")

        # extensions we check for
        self.excel_ext = excel_ext
        self.csv_ext = csv_ext

        if source is None:
            raise ValueError(f"{source=} should not be None")

        try:
            if source['Root'] is None:
                raise ValueError(f"need root directory in {source=}")
        except KeyError:
            log.debug(f"{source=} invalid config")
            return None

        # read all files in the given root directory
        files = os.listdir(source['Root'])
        rootdir = source['Root']

        self.data: Dict = source

        for fname in source:

            # skip root key
            if not fname == 'Root':
                path = source[fname]
                log.debug(f"{path=}")

                # split paths into name + extension
                base, ext = os.path.splitext(path)
                fullbase = os.path.join(rootdir, base)

                try:

                    # look for json file in rootdir
                    if base + '.json' in files:
                        log.debug(f"preexisting json found for {base=}")
                        self.data[fname] = base + '.json'

                    else:
                        log.debug(f"generating json file for {base=}")

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
                        self.data[fname] = base + '.json'

                # handle alternate utf encodings
                except UnicodeDecodeError:
                    log.debug(f"loading {ext=} file with ISO-8859-1 encoding")
                    df = pd.read_csv(fullbase + ext, encoding="ISO-8859-1")
                    self.store_dataframe(fullbase, df)
                    self.data[fname] = base + '.json'

    def store_dataframe(self, name: str, df: pd.DataFrame) -> None:
        """Serializes a dataframe in JSON format.

        Args:
            name: Name of the file we want to save
            df: Dataframe to be serialized

        Returns:
            Name of the file that has been serialized
        """
        name = name + '.json'
        log.debug(f"{name=}")
        json = df.to_json(orient='index')
        with open(name, 'w') as json_file:
            json_file.write(json)

        return None
