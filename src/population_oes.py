"""Population reading from OES data.

Population is working
"""
import math
import os
from typing import Dict, List, Optional, Tuple

import confuse  # type: ignore
import numpy as np  # type: ignore
import pandas as pd  # type: ignore

from data import Data
from filtermodel import Filter
from load_csv import LoadCSV
from log import Log
from population import Population
from util import datetime_to_code, load_dataframe


class PopulationOES(Population):
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
        config: confuse.Configuration,
        filt: Filter,
        log_root: Optional[Log] = None,
    ):
        """Initialize.

        Read the paths in and create dataframes, generate mappings
        """
        super().__init__(config, log_root=log_root)
        self.log_root = log_root
        log = self.log

        log.debug(f"module {__name__=}")

        # get location and population from the filter
        self.location = filt.location
        try:
            if self.location["county"] is not None:
                self.location["county"] += " County"
        except KeyError:
            log.debug("invalid location input {self.location=}")
            return

        self.subpop = filt.subpop
        self.codes: list

        self.load_data(config, self.location)

    def load_data(self, config, location):
        """Do most of the initializing here.

        That way the stuff we don't want passed is hidden.
        """
        # extract the dataframes we need from the input files
        if config is not None:
            source = config["Paths"].get()
            source = LoadCSV(source=source).data
            oes_df = load_dataframe(
                os.path.join(source["Root"], source["OES"])
            )
            code_df = self.format_code(
                load_dataframe(os.path.join(source["Root"], source["CODE"]))
            )
            pop_df = load_dataframe(
                os.path.join(source["Root"], source["POP"])
            )
            xls_df = self.format_map(
                load_dataframe(os.path.join(source["Root"], source["XLS"]))
            )

        # initialize unsliced dataframe from oes data
        if location["county"] is None and location["state"] is None:
            df = self.create_country_df(oes_df)
        elif location["county"] is not None and location["state"] is not None:
            location["county"] = location["county"]
            df = self.create_county_df(location, oes_df, code_df, pop_df)
        else:
            df = self.create_state_df(location, oes_df)

        # filter the population
        if self.subpop == "healthcare":
            df = self.health_filter(df)

        elif self.subpop == "wa_tier2_opt1":
            df = self.wa_tier2_opt1_filter(df)

        elif self.subpop == "wa_tier2_opt2":
            df = self.wa_tier2_opt2_filter(df)

        # the actual data passed onto the model
        self.pop_detail_df = self.drop_code(df)
        self.population_pP_tr = Data(
            "population_pP_tr",
            config,
            log_root=self.log_root,
            p_index=list(self.pop_detail_df.index),
            P_index=["Size"],
            array=self.drop_code(df).to_numpy(),
        )

        pop_to_burn_df = self.pop_to_burn_rate(df, xls_df)
        self.pop_demand_per_unit_map_pd_um: Data = Data(
            "pop_demand_per_unit_map_pd_um",
            config,
            log_root=self.log_root,
            p_index=list(pop_to_burn_df.index),
            array=pop_to_burn_df.to_numpy(),
        )

        self.set_essential(xls_df, config)
        # detail_pd_arr = detail_pd_df["Size"].to_numpy()
        # self.pop_demand_per_unit_map_pd_um: Data = self.pop_to_burn_rate(
        #         df,
        #         map_df
        # )
        # map_labs, map_arr = self.create_map(df, map_df)

        # load into dictionary
        # df_dict = {}
        # df_dict["detail_pd_df"] = detail_pd_df
        # df_dict["detail_pd_arr"] = detail_pd_arr
        # df_dict["map_labs"] = map_labs
        # df_dict["map_arr"] = map_arr

    def format_code(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform dataframe transformations specific to list1_2020.xls.

        Args:
            df: A dataframe

        Returns:
            A transformed dataframe to match the format needed for this project
        """
        # Specify columns to bypass issues with underlining in original excel
        df.columns = [
            "CBSA Code",
            "MDC Code",
            "CSA Code",
            "CBSA Title",
            "Metropolitan/Micropolitan Statistical Area",
            "Metropolitan Division Title",
            "CSA Title",
            "County Equivalent",
            "State Name",
            "FIPS State Code",
            "FIPS County Code",
            "Central/Outlying County",
        ]

        # Select MSA, as this is what OES data is based off of
        df = df[
            df["Metropolitan/Micropolitan Statistical Area"]
            == "Metropolitan Statistical Area"
        ]

        # Drop data we don't need
        df = df.drop(
            [
                "MDC Code",
                "CSA Code",
                "Metropolitan Division Title",
                "Metropolitan/Micropolitan Statistical Area",
                "CSA Title",
                "FIPS State Code",
                "FIPS County Code",
                "Central/Outlying County",
            ],
            axis=1,
        )

        # Reset indices for aesthetic appeal
        df = df.reset_index(drop=True)

        return df

    def format_map(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manually slice the excel model to get protection level mappings.

        Args:
            df: The excel model loaded into a dataframe

        Returns:
            The dataframe sliced to give the mappings
        """
        # manually redo indexing and select the rows we need

        # TODO: need new sheet that isn't precariously sliced like this
        DF_COLUMNS = 2528
        DF_START = 2529
        DF_END = 3303

        df.columns = df.iloc[DF_COLUMNS]
        df = df.iloc[DF_START:DF_END]
        df = df[
            ["Washington SOT", "SOC", "Type", "Level", "Essential (0 lowest)"]
        ]

        # fix datetime objects and drop empty rows
        df["SOC"] = df["SOC"].apply(datetime_to_code)
        df = df.dropna(axis="rows").reset_index(drop=True)
        return df

    def pop_to_burn_rate(
        self, df: pd.DataFrame, map_df: pd.DataFrame
    ) -> Tuple[list, np.ndarray]:
        """Generate mappings for OCC codes and population levels.

        Args:
            df: A dataframe that has OCC codes

        Returns:
            Dictionary of the population level mappings
        """
        map_arr = []
        labels = []
        for code in df["occ_code"]:
            arr = np.zeros(7)
            try:
                ind = map_df[map_df["SOC"] == code].index[0]
                level = map_df.iloc[ind]["Level"]
            except IndexError:
                if code.startswith("29-") or code.startswith("31-"):
                    level = 5.5
                else:
                    level = 3

            # assign integer levels
            if type(level) is int:
                arr[level] = 1

            # assign multiple levels
            else:
                arr[math.floor(level)] = 0.5
                arr[math.ceil(level)] = 0.5

            # add to dictionary
            name = df[df["occ_code"] == code].index.tolist()[0]
            labels.append(name)
            map_arr.append(arr)

        pop_to_level_df = pd.DataFrame(map_arr, index=labels)

        return pop_to_level_df

    def find_code(self, location: Dict, code_df: pd.DataFrame) -> int:
        """Finds the MSA code of given county.

        Args:
            None

        Returns:
            Integer corresponding to the given county's MSA code
        """
        if code_df is None:
            raise ValueError(f"{code_df=} should not be None")

        return int(
            code_df[
                (code_df["County Equivalent"] == location["county"])
                & (code_df["State Name"] == location["state"])
            ]["CBSA Code"].iloc[0]
        )

    def calculate_proportions(
        self,
        code: int,
        location: Dict,
        code_df: pd.DataFrame,
        pop_df: pd.DataFrame,
    ) -> float:
        """Calculate county proportion relative to total MSA pop.

        Args:
            code: MSA code for desired county

        Returns:
            A float corresponding to the ratio of the county's population in
            relation to its MSA code.
        """
        if code_df is None:
            raise ValueError(f"{code_df=} should not be None")
        if pop_df is None:
            raise ValueError(f"{code_df=} should not be None")

        # List the counties in the same MSA code as cty_name
        counties = list(
            code_df[code_df["CBSA Code"] == str(code)]["County Equivalent"]
        )

        # Construct dictionary mapping county names to constituent populations
        populations = {}
        for county in counties:
            pop = int(
                pop_df[
                    (pop_df["CTYNAME"] == county)
                    & (pop_df["STNAME"] == location["state"])
                ]["POPESTIMATE2019"]
            )
            populations[county] = pop

        # Calculate total population in MSA code
        total_pop = sum(populations.values())

        # Divide individual county population by total MSA population
        return populations[location["county"]] / total_pop

    def load_county(
        self,
        location: Dict,
        oes_df: pd.DataFrame,
        code_df: pd.DataFrame,
        pop_df: pd.DataFrame,
    ) -> Tuple[float, pd.DataFrame]:
        """Slice the OES data by county for further processing downstream.

        Args:
            None

        Returns:
            proportion: Float corresponding to proportion of residents from
                        MSA code living in given county
            df: Sliced OES dataframe
        """
        # find county MSA CODE
        code = self.find_code(location, code_df)

        # calculate proportion of MSA code's residents living in county
        proportion = self.calculate_proportions(
            code, location, code_df, pop_df
        )

        # initialize dataframe as slice of OES data
        df = oes_df[oes_df["area"] == code][
            ["occ_code", "occ_title", "o_group", "tot_emp"]
        ]

        # replace placeholders with 0
        df = df.replace(to_replace="**", value=0)

        return proportion, df

    def load_state(self, location: Dict, oes_df: pd.DataFrame) -> pd.DataFrame:
        """Slice the OES data by state for further processing downstream.

        Args:
            None

        Returns:
            df: Sliced OES dataframe
        """
        # slice OES dataframe by state
        col_list = ["occ_code", "occ_title", "o_group", "tot_emp"]
        df = oes_df[(oes_df["area_title"] == location["state"])][col_list]

        # replace placeholders with 0
        df = df.replace(to_replace="**", value=0)

        return df

    def load_country(self, oes_df: pd.DataFrame) -> pd.DataFrame:
        """Get the OES data for the whole country.

        The default setting for OES population
        """
        # slice OES dataframe by the whole county
        col_list = ["occ_code", "occ_title", "o_group", "tot_emp", "naics"]
        df = oes_df[
            (oes_df["area_title"] == "U.S.") & (oes_df["naics"] == "000000")
        ][col_list]
        df = df.drop(["naics"], axis=1)
        # replace placeholders with 0
        df = df.replace(to_replace="**", value=0)

        return df

    def fill_uncounted(
        self, major: pd.DataFrame, detailed: pd.DataFrame
    ) -> pd.DataFrame:
        """Create special categories for uncounted employees.

        Args:
            major: Dataframe containing totals for major OCC categories
            detailed: Dataframe containing totals for detailed OCC categories

        Returns:
            The detailed dataframe with extra categories to account for
            uncounted workers
        """
        code_list = list(set(major["occ_code"]))

        for code in code_list:
            pat = code[0:3]
            filt = detailed[detailed["occ_code"].str.startswith(pat)]

            # Calculate number of employees unaccounted for within the major
            # OCC code
            total = int(major[major["occ_code"] == code]["tot_emp"])
            det_total = np.sum(filt["tot_emp"])
            delta = total - det_total

            if delta > 0:
                # create dataframe row and append to detailed dataframe
                name = list(major[major["occ_code"] == code]["occ_title"])[0]
                add_lst = [
                    [pat + "XXXX", "Uncounted " + name, "detailed", delta]
                ]
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
        df = df.drop(df[df["tot_emp"] == 0].index)
        df = df.drop(["o_group"], axis=1)
        df = df.reset_index(drop=True)

        return df

    def drop_code(self, df: pd.DataFrame) -> pd.DataFrame:
        """Drop the OCC code from a dataframe.

        So that it has the right format for the model.
        """
        col_labs = ["Size"]
        self.codes = list(df["occ_code"])
        df = df.drop(["occ_code"], axis=1)
        df.columns = col_labs

        return df

    def create_county_df(
        self,
        location: Dict,
        oes_df: pd.DataFrame,
        code_df: pd.DataFrame,
        pop_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """Generate dataframe containing processed OES data by county.

        Args:
            None

        Returns:
            The processed dataframe
        """
        # Load in sliced dataframe
        proportion, df = self.load_county(location, oes_df, code_df, pop_df)

        # Split into 'major' and 'detailed' OCC categories
        major = df[df["o_group"] == "major"].copy()
        detailed = df[df["o_group"] == "detailed"].copy()

        # Some detailed categories don't have information availble - remove
        # these and place into "Uncounted" category
        detailed = self.fill_uncounted(major, detailed)

        # Adjust 'tot_emp' columns by MSA code proportion
        detailed["tot_emp"] = detailed["tot_emp"].apply(
            lambda x: int(x * proportion)
        )

        # Format to fit model
        detailed = self.format_output(detailed)
        detailed.set_index("occ_title", drop=True, inplace=True)
        return detailed

    def create_state_df(
        self, location: Dict, oes_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Generate dataframe containing processed OES data by state.

        Args:
            None

        Returns:
            The processed dataframe
        """
        # Load in sliced dataframe
        df = self.load_state(location, oes_df)

        major = df[df["o_group"] == "major"].copy()
        detailed = df[df["o_group"] == "detailed"].copy()

        # Some detailed categories don't have information available - remove
        # these and place into "Uncounted" category
        detailed = self.fill_uncounted(major, detailed)

        # Format to fit model
        detailed = self.format_output(detailed)
        detailed.set_index("occ_title", drop=True, inplace=True)
        return detailed

    def create_country_df(self, oes_df: pd.DataFrame) -> pd.DataFrame:
        """Generate dataframe containing processed OES data for US.

        Args:
            oes_df: Dataframe containing OES data

        Returns:
            The processed dataframe
        """
        df = self.load_country(oes_df)
        major = df[df["o_group"] == "major"].copy()
        detailed = df[df["o_group"] == "detailed"].copy()
        detailed = self.fill_uncounted(major, detailed)
        detailed = self.format_output(detailed)
        detailed.set_index("occ_title", drop=True, inplace=True)
        return detailed

    def health_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a detailed breakdown of healthcare workers with OCC codes.

        Args:
            None

        Returns:
            Dataframe object with the detailed breakdown
        """
        # 29-XXXX and 31-XXXX are the healthcare worker codes
        filt = df[
            (df["occ_code"].str.startswith("29-"))
            | (df["occ_code"].str.startswith("31-"))
        ]
        return filt

    def wa_tier2_opt1_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a detailed breakdown of Washington tier 2 workers.

        Args:
            None

        Returns:
            Dataframe object with the detailed breakdown
        """
        filt = df[
            (df["occ_code"].str.startswith("33-"))
            | (df["occ_code"].str.startswith("29-"))
            | (df["occ_code"].str.startswith("31-"))
        ]

        return filt

    def wa_tier2_opt2_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return a detailed breakdown of Washington tier 2 workers.

        Args:
            None

        Returns:
            Dataframe object with the detailed breakdown
        """
        occ_list = [
            "29-1292",
            "29-2040",
            "29-1215",
            "29-1126",
            "29-1223",
            "29-1181",
            "29-1221",
            "31-1120",
            "31-1131",
            "39-4031",
            "31-1132",
            "39-4011",
            "31-1133",
            "33-2011",
            "31-9091",
            "33-3012",
            "33-3021",
            "33-9093",
            "33-3041",
            "33-3051",
            "33-3052",
            "29-2052",
        ]

        filt = df[df["occ_code"].isin(occ_list)]

        return filt

    def set_essential(self, df: pd.DataFrame, config) -> pd.DataFrame:
        """Get population essential levels from the excel model.

        Manually slice the dataframe
        """
        # df.columns = df.iloc[2528]
        # df = df.iloc[2529:3303]
        # df = df[["SOC", "Essential (0 lowest)"]]

        pop_level: List = []
        df["SOC"] = df["SOC"].apply(datetime_to_code)
        df.reset_index(drop=True, inplace=True)

        for code in list(self.codes):
            arr = np.zeros(2)
            try:
                ind = df[df["SOC"] == code].index[0]
            except IndexError:
                ind = -1
            if ind > 0:
                level = df.iloc[ind]["Essential (0 lowest)"]
            else:
                level = np.random.randint(0, high=6)
            if level >= 5:
                arr[0] = 1
            else:
                arr[1] = 1
            pop_level.append(arr)

        self.pop_to_popsum1_per_unit_map_pp1_us = Data(
            "pop_to_popsum1_per_unit_map_pp1_us",
            config,
            log_root=self.log_root,
            p_index=list(self.pop_detail_df.index),
            array=np.array(pop_level),
        )
