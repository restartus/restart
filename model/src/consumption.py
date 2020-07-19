"""Consumption Model.

Consumption modeling
"""
import math
import logging
import pandas as pd  # type: ignore # noqa: F401
import numpy as np  # type: ignore # noqa: F401
from base import Base
from modeldata import ModelData
from util import Log, set_dataframe, datetime_to_code
from typing import Optional, Tuple
from population import Population
from resourcemodel import Resource


class Consumption(Base):
    """Calculate consumption based on Population and Resource.

    Take in Pop and and Res and into model.data["Pop Res Demand pn"]
    Some parameters are to use:
    - Washington estimate
    - Mitre burn rates
    - Johns Hopkins burn rates
    - CDPH estimates
    - Ensemble

    If pop and res aren't set by default take the existing Population and
    resource already in the model.data

    With dimensions ["Population p"]["Resource n"]

    This uses https://realpython.com/documenting-python-code/
    docstrings using the NumPy/SciPy syntax
    Uses a modified standard project
    Uses https://www.sphinx-doc.org/en/master/ to generate the documentation
    """

    def __init__(
        self,
        data: ModelData,
        pop: Population = None,
        res: Resource = None,
        log_root: Optional[Log] = None,
        type: Optional[str] = None,
    ):
        """Initialize the Economy object.

        This uses the Frame object and populates it with default data unless yo
        override it
        """
        # https://stackoverflow.com/questions/1385759/should-init-call-the-parent-classs-init/7059529
        super().__init__(log_root=log_root)

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
            # the sample code to move up the logging for a period
            log_root.con.setLevel(logging.DEBUG)
            log.debug(f"in {__name__=}")
            log_root.con.setLevel(logging.WARNING)
        else:
            log = logging.getLogger(__name__)
        self.log = log

        if pop is None:
            log.warning("Not implemented, if no pop passed, use model.data")
            return
        if res is None:
            log.warning("Not implemented, if no res passed, use model.data")
            return
        if type == "Mitre":
            log.debug("Use Mitre consumption")
        elif type == "Johns Hopkins":
            log.debug("Use JHU burn rate model")
        else:
            log.debug("For anything else use Washington data")

        # the same thing in a function less code duplication
        # note these are defaults for testing
        # this is the protection level and the burn rates for each PPE
        # use get to get a null
        # https://stackoverflow.com/questions/6130768/return-none-if-dictionary-key-is-not-available
        self.res_demand_mn_arr = data.value["Consumption m"][
            "Cons Resource mn"
        ]
        # self.res_demand_mn_arr = data.value["Resource Demand mn"]
        self.res_demand_mn_df = set_dataframe(
            self.res_demand_mn_arr,
            data.label,
            index="Consumption m",
            columns="Resource n",
        )
        log.debug(f"{self.res_demand_mn_df=}")
        # for compatiblity both the model and the object hold the same
        # description
        self.set_description(
            f"{self.res_demand_mn_df=}",
            data.description["Consumption m"]["Cons Resource mn"],
        )

        self.level_pm_arr = pop.map_arr
        # self.level_pm_arr = data.value["Population p"]["Protection pm"]
        '''
        self.level_pm_df = set_dataframe(
            self.level_pm_arr,
            data.label,
            index="Population p",
            columns="Consumption m",
        )
        '''
        # TODO: do this using set_dataframe and figure out labelling
        self.level_pm_df = pd.DataFrame(
                self.level_pm_arr,
                index=pop.map_labs,
                columns=data.label["Consumption m"]
        )

        log.debug(f"{self.level_pm_df=}")
        self.set_description(
            f"{self.level_pm_df=}",
            data.description["Population p"]["Protection pm"],
        )
        log.debug(f"{self.description['level_pm_df']=}")

        # TODO: we need to decide if all the data lives in data.value["Res
        # Demand mn"] or should it be gotten from classes like pop.demand_pn_df
        # As we mix both together, this is a philosophical thing as data.value
        # in effect makes everything a global, but passing classes hides
        # information. So data.value is great as an output, but now we are
        # duplicating information and increasing bugs

        self.demand_pn_df = self.level_pm_df @ self.res_demand_mn_df
        log.debug(f"{self.demand_pn_df=}")
        self.demand_pn_df.index.name = "Population p"
        self.demand_pn_df.columns.name = "Resource n"
        self.set_description(
            f"{self.demand_pn_df=}",
            data.description["Population p"]["Population Demand pn"],
        )

        self.level_pl_arr = np.hstack(
                (np.ones((pop.attr_pd_df.shape[0], 1)),
                 np.zeros((pop.attr_pd_df.shape[0], 1))))

        self.level_pl_df = pd.DataFrame(
                self.level_pl_arr,
                index=pop.map_labs,
                columns=data.label["Pop Level l"]
        )
        log.debug(f"{self.level_pl_df=}")
        '''
        self.level_pl_df = set_dataframe(
                self.level_pl_arr,
                data.label,
                index=,
                columns="Pop Level l",
                )
        '''
        # self.level_demand_ln_df = pop.level_pl_df.T @ self.demand_pn_df
        self.level_demand_ln_df = self.level_pl_df.T @ self.demand_pn_df
        log.debug(f"{self.level_demand_ln_df=}")
        self.set_description(
            f"{self.level_demand_ln_df=}",
            data.description["Population p"]["Level Demand ln"],
        )
        # now to the total for population
        # TODO: eventually demand will be across pdn so
        # across all the values
        # https://stackoverflow.com/questions/54786574/mypy-error-on-dict-of-dict-value-of-type-object-is-not-indexable
        # you need a casting just to tell it you are getting
        # https://docs.python.org/3/library/typing.html

        n95 = np.array(
                self.demand_pn_df['N95 Surgical'] * pop.attr_pd_arr).reshape(
                        [pop.attr_pd_arr.shape[0], 1])

        astm = np.array(
                self.demand_pn_df['ASTM Mask'] * pop.attr_pd_arr).reshape(
                        [pop.attr_pd_arr.shape[0], 1])
        self.total_demand_pn_arr = np.hstack((n95, astm))
        self.total_demand_pn_df = pd.DataFrame(
                self.total_demand_pn_arr,
                index=pop.map_labs,
                columns=data.label["Resource n"],
        )

        self.total_demand_pn_df.index.name = "Population p"
        '''
        self.total_demand_pn_df = (
            self.demand_pn_df
            * pop.attr_pd_df["Size"].values  # type: ignore
            # use below if the array is 1-D
            # self.demand_pn_df * self.attr_pd_arr
        )
        '''
        log.debug(f"{self.total_demand_pn_df=}")
        # convert to demand by levels note we have to transpose
        self.set_description(
            f"{self.total_demand_pn_df=}",
            data.description["Population p"]["Population Total Demand pn"],
        )
        self.level_total_demand_ln_df = (
            self.level_pl_df.T @ self.total_demand_pn_df
        )
        log.debug(f"{self.level_total_demand_ln_df=}")
        self.set_description(
            f"{self.level_total_demand_ln_df=}",
            data.description["Population p"]["Level Total Demand ln"],
        )
        # set to null to make pylint happy and instatiate the variable
        self.level_total_cost_ln_df = None
        self.set_description(
            f"{self.level_total_cost_ln_df=}",
            data.description["Population p"]["Level Total Cost ln"],
        )

    def level_total_cost(self, cost_ln_df):
        """Calculate the total cost of resource for a population level.

        The total cost of resources
        """
        log = self.log
        self.level_total_cost_ln_df = (
            self.level_total_demand_ln_df * cost_ln_df.values
        )
        log.debug("level_total_cost_ln_df\n%s", self.level_total_cost_ln_df)

        # method chaining
        return self

    def format_map(self, df: pd.DataFrame) -> pd.DataFrame:
        """Manually slice the excel model to get protection level mappings>

        Args:
            df: The excel model loaded into the dataframe

        Returns:
            The dataframe sliced to give the mappings
        """
        # manually redo indexing and select the rows we need
        df.columns = df.iloc[2528]
        df = df.iloc[2529:3303]
        df = df[['Washington SOT', 'SOC', 'Type', 'Level']]

        # fix datetime objects and drop empty rows
        df['SOC'] = df['SOC'].apply(datetime_to_code)
        df = df.dropna(axis='rows').reset_index(drop=True)
        return df

    def create_map(self, df: pd.DataFrame) -> Tuple[list, np.ndarray]:
        """Generate mappings for OCC codes and population levels.

        Args:
            df: A dataframe that has OCC codes

        Returns:
            Dictionary of the population level mappings
        """
        map_arr = []
        labels = []
        for code in df['occ_code']:
            arr = np.zeros(7)
            try:
                ind = self.map_df[self.map_df['SOC'] == code].index[0]
                level = self.map_df.iloc[ind]['Level']
            except IndexError:
                if code.startswith('29-') or code.startswith('31-'):
                    level = 5.5
                else:
                    level == 3

            # assign integer levels
            if type(level) is int:
                arr[level] = 1

            # assign multiple levels
            else:
                arr[math.floor(level)] = 0.5
                arr[math.ceil(level)] = 0.5

            # add to dictionary
            name = list(df[df['occ_code'] == code]['occ_title'])[0]
            labels.append(name)
            map_arr.append(arr)

        return labels, np.array(map_arr)
