import os
import pickle
import pandas as pd

OES_PATH = '../../../../../data/ingestion/all_data_M_2019.xlsx'
CODE_PATH = '../../../../../data/ingestion/list1_2020.xls'
POP_PATH = '../../../../../data/ingestion/co-est2019-alldata.csv'


class LoaderCSV():

    def __init__(self, *files):
        """Converts Excel and CSV files into dataframe objects. If you give
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

        self.splitpaths = []
        self.p_list = []

        # If passed CSV/Excel files, will convert to dataframe and then stash
        # in self.p_list. If passed pickle-files, skip conversion and directly
        # stash in self.p_list
        for file in files:

            # Split paths into name + extension and add to self.splitpaths
            splitpath = os.path.splitext(file)
            self.splitpaths.append(splitpath)

            # Load either CSV or Excel files into a dataframe
            ftype = splitpath[1]

            try:

                # Load Excel or CSV files into dataframes
                if ftype == '.xlsx' or ftype == '.xls':
                    df = pd.read_excel(file)
                    p_name = self.store_dataframe(splitpath[0], df)
                    self.p_list.append(p_name)
                elif ftype == '.csv':
                    df = pd.read_csv(file)
                    p_name = self.store_dataframe(splitpath[0], df)
                    self.p_list.append(p_name)

                # If passed pickle-file, do nothing
                elif ftype == '.p':
                    self.p_list.append(file)

                else:
                    raise TypeError('Invalid files')

            # Handle CSV files with UTF encoding incompatible with default
            except UnicodeDecodeError:
                df = pd.read_csv(file, encoding="ISO-8859-1")
                p_name = self.store_dataframe(splitpath[0], df)
                self.p_list.append(p_name)

    def store_dataframe(self, name: str, df: pd.DataFrame):
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
