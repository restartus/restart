"""Loader CSV.

The loader for the CSV
"""
import os
import pickle
import pandas as pd  # type:ignore
from loader.load import Load
from typing import List


class LoaderCSV(Load):
    """Converts Excel and CSV files into dataframe objects.

    If you give it files with a .xlsx, .xls, or .csv extension, it will read
    their data into a dataframe, and then save the dataframe as
    a pickle-file with the extension .p. If you feed this class
    a pickle-file, it will simply pass through this class. This is
    done so that we can minimize the amount of times the Excel/CSV
    data must be processed - for larger files, it can be lengthy.

    Attributes:
        splitpaths: List of tuples with format (path/to/file, extension)
        p_list: A list that becomes populated with the names of
                pickle-files containing the input-data in dataframe form.
    """

    def __init__(self, *paths,
                 excel_ext: List[str] = ['.yaml', 'yml'],
                 csv_ext: List[str] = ['csv']):
        """Initialize the Loader to read files.

        Reads the files
        """
        super().__init__()

        # Extensions we check for
        self.excel_ext = excel_ext
        self.csv_ext = csv_ext

        self.splitpaths = []
        self.p_list = []

        # If passed CSV/Excel files, will convert to dataframe and then stash
        # in self.p_list. If passed pickle-files, skip conversion and directly
        # stash in self.p_list
        for path in paths:

            # Split paths into name + extension and add to self.splitpaths
            splitpath = os.path.splitext(path)
            self.splitpaths.append(splitpath)

            # Load either CSV or Excel files into a dataframe
            ftype = splitpath[1]
            try:

                # Load Excel or CSV files into dataframes
                if ftype in self.excel_ext:
                    df = pd.read_excel(path)
                    p_name = self.store_dataframe(splitpath[0], df)
                    self.p_list.append(p_name)
                elif ftype in self.csv_ext:
                    df = pd.read_csv(path)
                    p_name = self.store_dataframe(splitpath[0], df)
                    self.p_list.append(p_name)

                # If passed pickle-file, do nothing
                elif ftype == '.p':
                    self.p_list.append(path)

                else:
                    raise TypeError('Invalid files')

            # Handle CSV files with UTF encoding incompatible with default
            except UnicodeDecodeError:
                df = pd.read_csv(path, encoding="ISO-8859-1")
                p_name = self.store_dataframe(splitpath[0], df)
                self.p_list.append(p_name)

    def store_dataframe(self, name: str, df: pd.DataFrame) -> str:
        """Pickles a dataframe.

        Args:
            name: Name of the file we want to save
            df: Dataframe we're pickling

        Returns:
            Name of the file that has been pickled
        """
        name = name + '.p'
        picklefile = open(name, 'ab')
        pickle.dump(df, picklefile)
        picklefile.close()

        return name
