"""The Resource Model.

Reads from dictionary for defaults
"""
import logging

import confuse  # type: ignore
import numpy as np  # type: ignore

from resourcemodel import Resource
from util import Log, set_dataframe


class ResourceDict(Resource):
    """ResourceDict - pulls resources from the default config yaml files.

    This can be a default for testing
    """

    def __init__(
        self, config: confuse.Configuration, log_root: Log = None,
    ):
        """Initialize the resources.

        Reads from the default config yaml files
        """
        # to pick up the description
        super().__init__(config, log_root=log_root)

        # create a sublogger if a root exists in the model
        self.log_root = log_root
        if log_root is not None:
            log = log_root.log_class(self)
        else:
            log = logging.getLogger(__name__)
        self.log = log
        self.log.debug(f"in {__name__}")

        # need labels for later since we do not have access to model
        self.label = config["Label"].get()

        self.attr_na_arr = config["Data"]["Resource n"][
            "Res Attr Data na"
        ].get()
        self.attr_na_df = set_dataframe(
            self.attr_na_arr,
            config["Label"].get(),
            index="Resource n",
            columns="Res Attribute a",
        )
        self.attr_na_df.index.name = "Resources n"
        self.attr_na_df.columns.name = "Res Attr a"
        log.debug(f"{self.attr_na_df=}")
        self.set_description(
            f"{self.attr_na_df=}",
            config["Description"]["Resource n"]["Res Attr Data na"].get(),
        )

        self.cost_ln_arr = config["Data"]["Resource n"][
            "Pop Level Res Cost ln"
        ].get()
        self.cost_ln_df = self.res_dataframe(np.array(self.cost_ln_arr))
        log.debug(f"{self.cost_ln_df=}")
        self.set_description(
            f"{self.cost_ln_df=}",
            config["Description"]["Resource n"]["Pop Level Res Cost ln"].get(),
        )

        self.inv_initial_ln_arr = config["Data"]["Resource n"][
            "Res Inventory Initial ln"
        ].get()
        self.inv_initial_ln_df = self.res_dataframe(
            np.array(self.inv_initial_ln_arr)
        )
        log.debug(f"{self.inv_initial_ln_df=}")
        self.set_description(
            f"{self.inv_initial_ln_df=}".split("=")[0],
            config["Description"]["Resource n"][
                "Res Inventory Initial ln"
            ].get(),
        )
        log.debug(f"{self.description['inv_initial_ln_df']}")
        # be careful you want a copy here so inv_initial stays the same
        self.inventory_ln_df = self.inv_initial_ln_df.copy()
        log.debug(f"Setting initial inventory {self.inventory_ln_df=}")
        self.set_description(
            f"{self.inventory_ln_df=}".split("=")[0],
            config["Description"]["Resource n"]["Res Inventory ln"].get(),
        )

        self.inv_eoc_ln_arr = config["Data"]["Resource n"][
            "Res Inventory EOC ln"
        ].get()
        log.debug(f"{self.inv_eoc_ln_arr=}")
        self.inv_eoc_ln_df = self.res_dataframe(np.array(self.inv_eoc_ln_arr))
        # ensure we don't have any non-zero numbers
        self.inv_eoc_ln_df[self.inv_eoc_ln_df < 1] = 1
        log.debug(f"{self.inv_eoc_ln_df=}")
        self.set_description(
            f"{self.inv_eoc_ln_df=}",
            config["Description"]["Resource n"]["Res Inventory EOC ln"].get(),
        )
        log.debug(f"{self.description['inv_eoc_ln_df']}")

        # TODO: inv_min_rln should use to be written own own DataFrame
        self.inv_min_rln_arr = config["Data"]["Resource n"][
            "Res Inventory Min ln"
        ].get()
        self.inv_min_rln_df = self.res_dataframe(
            np.array(self.inv_min_rln_arr)
        )
        self.set_description(
            f"{self.inv_min_rln_df=}",
            config["Description"]["Resource n"]["Res Inventory Min ln"].get(),
        )

        self.inv_min_in_periods_arr = config["Data"]["Resource n"][
            "Res Inventory Min in Periods ln"
        ].get()
        self.inv_min_in_periods_df = self.res_dataframe(
            np.array(self.inv_min_in_periods_arr)
        )
        self.set_description(
            f"{self.inv_min_in_periods_df=}",
            config["Description"]["Resource n"][
                "Res Inventory Min in Periods ln"
            ].get(),
        )
