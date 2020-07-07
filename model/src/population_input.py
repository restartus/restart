import os
import pickle
import pandas as pd
import numpy as np
from population import Population

OES_PATH = '~/ws/git/data/ingestion/all.p'
CODE_PATH = '~/ws/git/data/ingestion/code.p'
POP_PATH = '~/ws/git/data/ingestion/pop.p'


class PopulationInput(Population):
    """Extracts OES data from BLS, and combines this with Census population
       data by county to estimate the number of employees in each OCC code for
       the county.

    Attributes:
        cty_name: Name of county you want stats for
        state_name: Name of state that county is in
        model: Default Bharat model for now
        attr_df: Pandas dataframe with sliced and adjusted OES data
    """

    def __init__(self, model, cty_name=None, state_name=None,
                 oes_file=os.path.expanduser(OES_PATH),
                 code_file=os.path.expanduser(CODE_PATH),
                 pop_file=os.path.expanduser(POP_PATH)):

        self.cty_name = 'Santa Cruz County'
        self.state_name = 'California'
        self.model = model

        self.df = self.create_df(oes_file, code_file, pop_file)

        super().__init__(model=self.model)

    def find_code(self, code_df):
        """Finds the MSA code of the county specified by self.cty_name and
           self.state_name.

        Args:
            code_df: Pandas dataframe containing counties within MSA

        Returns:
            Integer corresponding to the the given county's MSA code.
        """

        return int(code_df[(code_df['County Equivalent'] == self.cty_name) &
                   (code_df['State Name'] == self.state_name)]
                   ['CBSA Code'].iloc[0])

    def calculate_proportions(self, code, code_df, pop_df):
        """Given a US county and state, calculates the ratio of the county's
           population in relation to its MSA code. Provides a multiplier for
           us to scale OES data by.

        Args:
            code: MSA code for desired county
            code_df: Pandas dataframe containing counties within MSA
            pop_df: Pandas dataframe containing county population data

        Returns:
            A float corresponding to the ratio of the county's population in
            relation to its MSA code.
        """

        # List the counties in the same MSA code as cty_name
        counties = list(code_df[code_df['CBSA Code'] == str(code)]
                               ['County Equivalent'])

        # Construct a dictionary mapping county names to their
        # constituent populations
        populations = {}
        for county in counties:
            pop = int(pop_df[(pop_df['CTYNAME'] == county)
                             & (pop_df['STNAME'] == self.state_name)]
                            ['POPESTIMATE2019'])
            populations[county] = pop

        # Calculate the total population in the MSA code
        total_pop = sum(populations.values())

        # Divide the individual county's population by the total MSA
        # population to get the proportion
        return populations[self.cty_name] / total_pop

    def create_df(self, oes_file, code_file, pop_file):
        """Given a US county and states, return relevant OES data.

        Args:
            oes_df: Pandas dataframe containing OES data
            code_df: Pandas dataframe containing counties within MSA
            pop_df: Pandas dataframe containing county census data

        Returns:
            detailed: Dataframe containing detailed OCC codes and the number
                      of employees that they contain. Codes with common
                      prefixes (e.g "11-" refer to similar occupations.
        """

        # Load dataframes
        oes_df = pickle.load(open(oes_file, 'rb'))
        code_df = pickle.load(open(code_file, 'rb'))
        pop_df = pickle.load(open(pop_file, 'rb'))

        # Find the county's MSA code
        code = self.find_code(code_df)

        # Calculate the proportion of that MSA code's residents residing in
        # the individual county
        proportion = self.calculate_proportions(code, code_df, pop_df)

        # Initialize the dataframe as a slice of all the OES data
        df = oes_df[oes_df['area'] == code][['occ_code', 'occ_title',
                                             'o_group', 'tot_emp']]

        # Split into 'major' and 'detailed' OCC categories
        major = df[df['o_group'] == 'major'].copy()
        detailed = df[df['o_group'] == 'detailed'].copy()

        # Generate a list of strings containing the major OCC codes
        code_list = list(major['occ_code'])

        # Some detailed categories don't have information available - remove
        # these and place into "Uncounted" category
        for code in code_list:

            # Search by code prefix (e.g "11-")
            pat = code[0:3]
            filt = detailed[detailed['occ_code'].str.startswith(pat)]

            # Calculate number of employees unaccounted for within the major
            # OCC code
            total = int(major[major['occ_code'] == code]['tot_emp'])
            det_total = np.sum(filt['tot_emp'])
            delta = total - det_total

            # Create a dataframe row and append this to the detailed DataFrame
            name = list(major[major['occ_code'] == code]['occ_title'])[0]
            add_lst = [[pat + 'XXXX', 'Uncounted ' + name, 'detailed', delta]]
            add_df = pd.DataFrame(add_lst, columns=list(major.columns))
            detailed = detailed.append(add_df, ignore_index=True)

        # Adjust 'tot_emp' columns by MSA code proportion
        detailed['tot_emp'] = detailed['tot_emp'].apply(
                                lambda x: int(x * proportion))
        major['tot_emp'] = major['tot_emp'].apply(
                            lambda x: int(x * proportion))

        # Format to fit model
        detailed.drop(detailed[detailed['tot_emp'] == 0].index, inplace=True)
        detailed = detailed.drop(['occ_code', 'o_group'], axis=1)
        detailed.reset_index(drop=True, inplace=True)

        return detailed
