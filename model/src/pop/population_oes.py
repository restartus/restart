"""Population reading from OES data.

Population is working
"""
import pickle
import pandas as pd  # type: ignore
import numpy as np  # type: ignore
from typing import Optional, Tuple
from model import Model
from pop.population_dict import PopulationDict
from loader.load_csv import LoaderCSV

OES_PATH = '../../../../../data/ingestion/all_data_M_2019.p'
CODE_PATH = '../../../../../data/ingestion/list1_2020.p'
POP_PATH = '../../../../../data/ingestion/co-est2019-alldata.p'


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
    # note you should declare otherwise type lint fails
    # as the static module cannot tell the type in init()
    code_df: pd.DataFrame
    oes_df: pd.DataFrame
    pop_df: pd.DataFrame

    def __init__(
        self,
        model: Model,
        cty_name: Optional[str] = None,
        state_name: Optional[str] = None,
        index: Optional[str] = None,
        columns: Optional[str] = None,
        oes_path: str = OES_PATH,
        code_path: str = CODE_PATH,
        pop_path: str = POP_PATH
    ):
        """Initialize.

        Read the paths in and create dataframes
        """
        self.p_list = LoaderCSV(oes_path, code_path, pop_path).p_list

        # Format the dataframes
        df_list = []
        for fname in self.p_list:
            df_list.append(self.load_df(fname))

        # MSA code dataframe
        df_list[1] = self.format_code(df_list[1])

        # Extract the dataframes we need from the input files
        self.oes_df = df_list[0]
        self.code_df = df_list[1]
        self.pop_df = df_list[2]

        # Defaults for testing
        if cty_name is None and state_name is None:
            self.state_name = 'California'
            self.df = self.create_state_df()

        # Calculate for entire state
        if cty_name is None and state_name is not None:
            self.state_name = state_name
            self.df = self.create_state_df()

        # Calculate for specified county
        elif cty_name is not None and state_name is not None:
            self.cty_name = cty_name
            self.state_name = state_name
            self.df = self.create_county_df()

        self.tot_pop = np.sum(self.df['tot_emp'])
        self.health = self.healthcare_filter()
        self.occ = self.df.drop(['occ_code'], axis=1)
        super().__init__(model,
                         source=self.health,
                         index=index,
                         columns=columns)

    def load_df(self, fname: str) -> Optional[pd.DataFrame]:
        """Load a pickle-file into a dataframe.

        Args:
            fname: Name of a pickle-file

        Returns:
            The dataframe serialized in the pickle-file
        """
        try:
            df = pickle.load(open(fname, 'rb'))
            return df

        except FileNotFoundError:
            print("Invalid file")
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
            raise ValueError(f"{self.code_df=} should not be Ñone")
        return int(self.code_df[(self.code_df['County Equivalent'] ==
                   self.cty_name) & (self.code_df['State Name'] ==
                                     self.state_name)]['CBSA Code'].iloc[0])

    def calculate_proportions(self, code: int) -> float:
        """Calculate Proportion relative to MSA.

        Given a US county and state, calculate the ratio of the county's
           population in relation to its MSA code. Provides a multiplier for
           us to scale OES data by.

        Args:
            code: MSA code for desired county

        Returns:
            A float corresponding to the ratio of the county's population in
            relation to its MSA code.
        """
        # List the counties in the same MSA code as cty_name
        counties = list(self.code_df[self.code_df['CBSA Code'] == str(code)]
                                    ['County Equivalent'])

        # Construct dictionary mapping county names to constituent populations
        populations = {}
        for county in counties:
            pop = int(self.pop_df[(self.pop_df['CTYNAME'] == county)
                                  & (self.pop_df['STNAME'] == self.state_name)]
                                 ['POPESTIMATE2019'])
            populations[county] = pop

        # Calculate total population in MSA code
        total_pop = sum(populations.values())

        # Divide individual county population by total MSA population
        return populations[self.cty_name] / total_pop

    def load_county(self) -> Tuple[float, pd.DataFrame]:
        """Slice the OES data by county for further processing downstream.

        Args:
            None

        Returns:
            proportion: Float corresponding to proportion of residents from
                        MSA code living in given county
            df: Sliced OES dataframe
        """
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
        # Slice OES dataframe by state
        df = self.oes_df[(self.oes_df['area_title'] == self.state_name)][
                ['occ_code', 'occ_title', 'o_group', 'tot_emp']]

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
