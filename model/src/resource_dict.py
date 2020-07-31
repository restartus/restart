"""The Resource Model.

Reads from dictionary for defaults
"""
import logging

import numpy as np  # type: ignore

from modeldata import ModelData
from resourcemodel import Resource
from util import Log, set_dataframe


class ResourceDict(Resource):
    """ResourceDict - pulls resources from the default config yaml files.

    This can be a default for testing
    """

    def __init__(
        self, data: ModelData, log_root: Log = None,
    ):
        """Initialize the resources.

        Reads from the default config yaml files
        """
        # to pick up the description
        super().__init__(log_root=log_root)

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        self.log.debug(f"in {__name__}")

        # need labels for later since we do not have access to model
        self.label = data.label

        self.attr_na_arr = data.value["Resource n"]["Res Attr Data na"]
        self.attr_na_df = set_dataframe(
            self.attr_na_arr,
            data.label,
            index="Resource n",
            columns="Res Attribute a",
        )
        self.attr_na_df.index.name = "Resources n"
        self.attr_na_df.columns.name = "Res Attr a"
        log.debug(f"{self.attr_na_df=}")
        self.set_description(
            f"{self.attr_na_df=}",
            data.description["Resource n"]["Res Attr Data na"],
        )

        self.cost_ln_arr = data.value["Resource n"]["Pop Level Res Cost ln"]
        self.cost_ln_df = self.res_dataframe(np.array(self.cost_ln_arr))
        log.debug(f"{self.cost_ln_df=}")
        self.set_description(
            f"{self.cost_ln_df=}",
            data.description["Resource n"]["Pop Level Res Cost ln"],
        )

        self.inv_initial_ln_arr = data.value["Resource n"][
            "Res Inventory Initial ln"
        ]
        self.inv_initial_ln_df = self.res_dataframe(
            np.array(self.inv_initial_ln_arr)
        )
        log.debug(f"{self.inv_initial_ln_df=}")
        self.set_description(
            f"{self.inv_initial_ln_df=}".split("=")[0],
            data.description["Resource n"]["Res Inventory Initial ln"],
        )
        log.debug(f"{self.description['inv_initial_ln_df']}")
        # be careful you want a copy here so inv_initial stays the same
        self.inventory_ln_df = self.inv_initial_ln_df.copy()
        log.debug(f"Setting initial inventory {self.inventory_ln_df=}")
        self.set_description(
            f"{self.inventory_ln_df=}".split("=")[0],
            data.description["Resource n"]["Res Inventory ln"],
        )

        self.inv_eoc_ln_arr = data.value["Resource n"]["Res Inventory EOC ln"]
        log.debug(f"{self.inv_eoc_ln_arr=}")
        self.inv_eoc_ln_df = self.res_dataframe(np.array(self.inv_eoc_ln_arr))
        # ensure we don't have any non-zero numbers
        self.inv_eoc_ln_df[self.inv_eoc_ln_df < 1] = 1
        log.debug(f"{self.inv_eoc_ln_df=}")
        self.set_description(
            f"{self.inv_eoc_ln_df=}",
            data.description["Resource n"]["Res Inventory EOC ln"],
        )
        log.debug(f"{self.description['inv_eoc_ln_df']}")

        safety_stock_ln_arr = data.value["Resource n"][
            "Res Inventory Safety Stock ln"
        ]
        self.safety_stock_ln_df = self.res_dataframe(
            np.array(safety_stock_ln_arr)
        )
        self.set_description(
            f"{self.safety_stock_ln_df=}",
            data.description["Resource n"]["Res Inventory Safety Stock ln"],
        )

        self.average_demand_ln_arr = data.value["Resource n"][
            "Res Inventory Average Demand ln"
        ]
        self.average_demand_ln_df = self.res_dataframe(
            np.array(self.average_demand_ln_arr)
        )
        self.set_description(
            f"{self.average_demand_ln_df=}",
            data.description["Resource n"]["Res Inventory Average Demand ln"],
        )

        self.stockpile_days_ln_arr = data.value["Resource n"][
            "Res Inventory Stockpile Days ln"
        ]
        self.stockpile_days_ln_df = self.res_dataframe(
            np.array(self.stockpile_days_ln_arr)
        )
        self.set_description(
            f"{self.stockpile_days_ln_df=}",
            data.description["Resource n"]["Res Inventory Stockpile Days ln"],
        )
