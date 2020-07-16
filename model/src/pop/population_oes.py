"""Population reading from OES data.

Population is working
"""
import os
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from typing import Optional, Tuple, Dict
from util import Log
from pop.population_dict import PopulationDict
from loader.load_csv import LoadCSV


class PopulationOES(PopulationDict):
    """Transforms OES data into a format compatible with the model.

    Performs calculations to give us an estimate of population distributions on
       a county-wide basis.

    Attributes:
        oes_df: Dataframe containing OES data
        code_df: Dataframe containing conversions between county and MSA code
        pop_df: Dataframe containing census population data per county
        cty_name: Name of a US county
        state_name: Name of a US state
        df: The processed, OES data in a dataframe
    """

    def __init__(
        self,
        location: Dict,
        log_root: Optional[Log] = None,
        source: Optional[Dict] = None,
        index: Optional[str] = None,
        columns: Optional[str] = None,
    ):
        """Initialize.

        Read the paths in and create dataframes
        """
        self.root_log: Optional[Log]
        # global log
        # log: logging.Logger = logging.getLogger(__name__)

        if log_root is not None:
            self.log_root = log_root
            log = self.log = log_root.log_class(self)
            log.debug(f"{self.log=} {log=}")

        log.debug(f"module {__name__=}")

        # note you should declare otherwise type lint fails
        # as the static module cannot tell the type in init()
        self.code_df: pd.DataFrame
        self.oes_df: pd.DataFrame
        self.pop_df: pd.DataFrame

        # Extract the dataframes we need from the input files
        # TODO: source stream handling
        if source is not None:
            self.source = LoadCSV(source=source).data
            self.oes_df = self.load_df(os.path.join(source['Root'],
                                                    source['OES']))
            self.code_df = self.format_code(
                    self.load_df(os.path.join(source['Root'], source['CODE']))
                    )
            self.pop_df = self.load_df(os.path.join(source['Root'],
                                                    source['POP']))

        # Handle location input
        self.location = location
        log.debug(f"{self.location=}")

        # Need to specify a state
        if location["State"] is None:
            raise ValueError(f"invalid {self.location=} must specify state")

        # Looking for a specific county
        if location["County"] is not None and location["State"] is not None:
            self.df = self.create_county_df()

        # Looking for a whole state
        else:
            self.df = self.create_state_df()

        # Slicing for compatibility with rest of model
        self.tot_pop = np.sum(self.df['tot_emp'])
        self.health = self.healthcare_filter()
        self.occ = self.df.drop(['occ_code'], axis=1)

        # TODO: this isn't necessary - should probably just be a child of Base
        super().__init__(source=self.health,
                         index=index,
                         columns=columns)

    def load_df(self, fname: str) -> Optional[pd.DataFrame]:
        """Load h5 file into a dataframe.

        Args:
            fname: Name of h5 file

        Returns:
            The dataframe serialized in the h5 file
        """
        try:
            df: pd.DataFrame = pd.read_hdf(fname, 'df')
            return df

        except ValueError:
            self.log.debug(f"invalid file {fname=}")
            return None

    def format_code(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform dataframe transformations specific to list1_2020.xls.

        Args:
            df: A dataframe

        Returns:
            A transformed dataframe to match the format needed for this project
        """
        # Specify columns to bypass issues with underlining in original excel
        df.columns = ['CBSA Code', 'MDC Code', 'CSA Code', 'CBSA Title',
                      'Metropolitan/Micropolitan Statistical Area',
                      'Metropolitan Division Title', 'CSA Title',
                      'County Equivalent', 'State Name', 'FIPS State Code',
                      'FIPS County Code', 'Central/Outlying County']

        # Select MSA, as this is what OES data is based off of
        df = df[df['Metropolitan/Micropolitan Statistical Area'] ==
                'Metropolitan Statistical Area']

        # Drop data we don't need
        df = df.drop(['MDC Code', 'CSA Code',
                      'Metropolitan Division Title',
                      'Metropolitan/Micropolitan Statistical Area',
                      'CSA Title', 'FIPS State Code', 'FIPS County Code',
                      'Central/Outlying County'], axis=1)

        # Reset indeces for aesthetic appeal
        df = df.reset_index(drop=True)

        return df

    def find_code(self) -> int:
        """Finds the MSA code of given county.

        Args:
            None

        Returns:
            Integer corresponding to the given county's MSA code
        """
        if self.code_df is None:
            raise ValueError(f"{self.code_df=} should not be None")

        return int(self.code_df[(self.code_df['County Equivalent'] ==
                   self.location['County']) & (self.code_df['State Name'] ==
                                               self.location['State'])]
                   ['CBSA Code'].iloc[0])

    def calculate_proportions(self, code: int) -> float:
        """Calculate county proportion relative to total MSA pop.

        Args:
            code: MSA code for desired county

        Returns:
            A float corresponding to the ratio of the county's population in
            relation to its MSA code.
        """
        if self.code_df is None:
            raise ValueError(f"{self.code_df=} should not be None")
        if self.pop_df is None:
            raise ValueError(f"{self.code_df=} should not be None")

        # List the counties in the same MSA code as cty_name
        counties = list(self.code_df[self.code_df['CBSA Code'] == str(code)]
                                    ['County Equivalent'])

        # Construct dictionary mapping county names to constituent populations
        populations = {}
        for county in counties:
            pop = int(self.pop_df[(self.pop_df['CTYNAME'] == county)
                                  & (self.pop_df['STNAME'] ==
                                     self.location['State'])]
                                 ['POPESTIMATE2019'])
            populations[county] = pop

        # Calculate total population in MSA code
        total_pop = sum(populations.values())

        # Divide individual county population by total MSA population
        return populations[self.location['County']] / total_pop

    def load_county(self) -> Tuple[float, pd.DataFrame]:
        """Slice the OES data by county for further processing downstream.

        Args:
            None

        Returns:
            proportion: Float corresponding to proportion of residents from
                        MSA code living in given county
            df: Sliced OES dataframe
        """
        if self.oes_df is None:
            raise ValueError(f"{self.oes_df=} should not be None")

        # Find county MSA CODE
        code = self.find_code()

        # Calculate proportion of MSA code's residents living in county
        proportion = self.calculate_proportions(code)

        # Initialize dataframe as slice of OES data
        df = self.oes_df[self.oes_df['area'] == code][['occ_code', 'occ_title',
                                                       'o_group', 'tot_emp']]

        # Replace placeholders with 0
        df = df.replace(to_replace='**', value=0)

        return proportion, df

    def load_state(self) -> pd.DataFrame:
        """Slice the OES data by state for further processing downstream.

        Args:
            None

        Returns:
            df: Sliced OES dataframe
        """
        if self.oes_df is None:
            raise ValueError(f"{self.oes_df=} should not be None")

        # Slice OES dataframe by state
        col_list = ['occ_code', 'occ_title', 'o_group', 'tot_emp']
        df = self.oes_df[(self.oes_df['area_title'] ==
                          self.location['State'])][col_list]

        # Replace placeholders with 0
        df = df.replace(to_replace='**', value=0)

        return df

    def fill_uncounted(self, major: pd.DataFrame,
                       detailed: pd.DataFrame) -> pd.DataFrame:
        """Create special categories for uncounted employees.

        Args:
            major: Dataframe containing totals for major OCC categories
            detailed: Dataframe containing totals for detailed OCC categories

        Returns:
            The detailed dataframe with extra categories to account for
            uncounted workers
        """
        code_list = list(major['occ_code'])

        for code in code_list:
            pat = code[0:3]
            filt = detailed[detailed['occ_code'].str.startswith(pat)]

            # Calculate number of employees unaccounted for within the major
            # OCC code
            total = int(major[major['occ_code'] == code]['tot_emp'])
            det_total = np.sum(filt['tot_emp'])
            delta = total - det_total

            # Create dataframe row and append to detailed dataframe
            name = list(major[major['occ_code'] == code]['occ_title'])[0]
            add_lst = [[pat + 'XXXX', 'Uncounted ' + name, 'detailed', delta]]
            add_df = pd.DataFrame(add_lst, columns=list(major.columns))
            detailed = detailed.append(add_df, ignore_index=True)

        return detailed

    def format_output(self, df: pd.DataFrame) -> pd.DataFrame:
        """Format dataframe to fit the model by dropping some columns.

        Args:
            df: The dataframe we want to format

        Returns:
            The formatted dataframe
        """
        df = df.drop(df[df['tot_emp'] == 0].index)
        df = df.drop(['o_group'], axis=1)
        df = df.reset_index(drop=True)

        return df

    def create_county_df(self) -> pd.DataFrame:
        """Generate dataframe containing processed OES data by county.

        Args:
            None

        Returns:
            The processed dataframe
        """
        # Load in sliced dataframe
        proportion, df = self.load_county()

        # Split into 'major' and 'detailed' OCC categories
        major = df[df['o_group'] == 'major'].copy()
        detailed = df[df['o_group'] == 'detailed'].copy()

        # Some detailed categories don't have information availble - remove
        # these and place into "Uncounted" category
        detailed = self.fill_uncounted(major, detailed)

        # Adjust 'tot_emp' columns by MSA code proportion
        detailed['tot_emp'] = detailed['tot_emp'].apply(
                                lambda x: int(x * proportion))

        # Format to fit model
        detailed = self.format_output(detailed)

        return detailed

    def create_state_df(self) -> pd.DataFrame:
        """Generate dataframe containing processed OES data by state.

        Args:
            None

        Returns:
            The processed dataframe
        """
        # Load in sliced dataframe
        df = self.load_state()

        major = df[df['o_group'] == 'major'].copy()
        detailed = df[df['o_group'] == 'detailed'].copy()

        # Some detailed categories don't have information available - remove
        # these and place into "Uncounted" category
        detailed = self.fill_uncounted(major, detailed)

        # Format to fit model
        detailed = self.format_output(detailed)

        return detailed

    def healthcare_filter(self) -> pd.DataFrame:
        """Project OCC code into healthcare vs non-healthcare workers.

        Args:
            None

        Returns:
            Dataframe giving total healthcare and non-healthcare populations
        """
        # 29-NNNN and 31-NNNN are healthcare worker OCC codes
        filt = self.df[(self.df['occ_code'].str.startswith('29-')) |
                       (self.df['occ_code'].str.startswith('31-'))]

        # Dataframe labels
        col_labs = ['Population p', 'Size']

        # Calculate total number of healthcare workers
        tot_health = np.sum(filt['tot_emp'])
        health = [['Healthcare Workers', tot_health]]

        # Calculate total number of non-healthcare workers
        non_health = [['Non-Healthcare Workers', self.tot_pop - tot_health]]

        # Construct dataframes and append
        health_df = pd.DataFrame(health, columns=col_labs)
        non_health_df = pd.DataFrame(non_health, columns=col_labs)
        health_df = health_df.append(non_health_df, ignore_index=True)

        return health_df
