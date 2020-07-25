"""Dashboard for COVID.

## Stock demo
https://towardsdatascience.com/how-to-build-a-data-science-web-app-in-python-61d1bed65020
From https://github.com/restartus/demo-self-driving/blob/master/app.py
Use a main and a well formed way to run things

https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2
has more ways to do selects and tables

"""
# import logging  # noqa: F401

import logging
from typing import Dict

import altair as alt  # type:ignore

# https://mypy.readthedocs.io/en/latest/existing_code.html
import pandas as pd  # type:ignore
import streamlit as st  # type:ignore

from base import Base
from model import Model

# https://docs.python.org/3/howto/logging-cookbook.html
# logging.basicConfig(level=logging.DEBUG
# https://www.w3resource.com/python-exercises/python-basic-exercise-46.php
# https://www.geeksforgeeks.org/python-os-path-basename-method/
# name: str = os.path.basename(__file__).split(".")[0]


class Dashboard:
    """Dashboard object.

    Streamlit dashboard
    """

    def __init__(self, model: Model):
        """Display the decision dashboard.

        Streamlit dashboard for a Model
        """
        self.log_root = model.log_root
        if self.log_root is not None:
            log = self.log_root.log_class(self)
            log.debug(f"found {self.log_root=} and made {log=}")
        else:
            # backup logger
            log = logging.getLogger(__name__)
        self.log = log
        log.debug(f"{__name__=}")

        # sample test data
        self.data_df = pd.DataFrame(
            [[0, 123], [12, 23]],
            index=["healthcare", "Non-healthcare"],
            columns=["N95", "Mask"],
        )
        self.data_df.index.name = "Level l"
        self.data_df.columns.name = "Resource n"
        # https://stackoverflow.com/questions/1398022/looping-over-all-member-variables-of-a-class-in-python
        log.debug(f"{log=}")
        log.debug(f"{vars(model)=}")
        log.debug(f"{vars(model.population)}=")
        # https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python
        # this gives all kinds of things that are hidden functions;
        log.debug(f"{dir(model.population)=}")
        for name, value in vars(model).items():
            log.debug(f"{name=}")
            log.debug(f"{value=}")
            # http://notesbyanerd.com/2017/12/26/check-in-python-if-a-value-is-instance-of-a-custom-class/
            if isinstance(value, Base):
                log.debug(f"found ${value=} is Base")
        # the same thing using the odel iterator
        for name, value in model:
            log.debug(f"{name=} {value=}")

        # https://stackoverflow.com/questions/44790030/return-all-class-variable-values-from-a-python-class
        for name, value in vars(model.population).items():
            log.debug(f"{name=}")
            log.debug(f"{value=}")

        # Simple selection
        st.sidebar.markdown(
            """
            ## Pages
            Choose the page you want from here
            """
        )
        self.page = st.sidebar.selectbox(
            "Choose page",
            [
                "Exploration",
                "Tables",
                "Home",
                "Test Home",
                "Test Tables",
                "Test Exploration",
            ],
        )

        stockpile_days = st.sidebar.slider(
            "Stockpile", max_value=120, value=30
        )
        log.debug(f"{stockpile_days=}")

        model.resource.set_stockpile_days(stockpile_days)

        if self.page == "Home":
            self.home_page(model)
        elif self.page == "Tables":
            self.tables(model)
        elif self.page == "Exploration":
            self.visualize_model(model)
        elif self.page == "Test Tables":
            self.test_tables(model)
        elif self.page == "Test Home":
            self.test_home(self.data_df)
        elif self.page == "Test Exploration":
            st.title("Data Exploration")
            # https://docs.streamlit.io/en/latest/api.html
            st.dataframe(self.data_df)
            st.write(f"{self.data_df.index=}")
            st.write(f"{self.data_df.columns=}")
            x_axis = st.selectbox(
                "Choose x-axis", self.data_df.index, index=0
            )
            y_axis = st.selectbox(
                "Choose y-axis", self.data_df.columns, index=1
            )
            st.write(f"{x_axis=} {y_axis=}")
            x_multi = st.multiselect("Select Summary Levels",
                                     self.data_df.index)
            y_multi = st.multiselect("Select Resource to Display",
                                     self.data_df.columns)
            st.write(f"{x_multi=}")
            st.write(f"{y_multi=}")
            self.visualize_data(self.data_df, x_axis, y_axis)
            self.visualize_data(self.data_df, x_multi, y_multi)
            # Not that write uses Markdown

    def home_page(self, model):
        """Home page.

        # COVID-19 Decision Dashboard
        ## Restart.us
        Use caution when interpreting these numbers
        """

    # uses the literal magic in Streamlit 0.62
    # note that just putting an expression automatically wraps an st.write
    def test_tables(self, model):
        """Tables.

        The full graphical display of all tables use for debugging mainly
        """
        """
        # COVID-19 Decision Tool
        ## Restart.us
        The main data table in the model for your viewing please.
        These are all Pandas Dataframes for display. For multi-dimensional
        data, there will be both a Numpy Array for the tensor and a Multi-Index
        for display.

        When you are using these, as a hint, the row and column have distinct
        variable letters so you can keep it all straight in detailed data
        analysis.

        ###Resource safety Stock ln.

        The supply of resource needs
        """
        model.resource.safety_stock_ln_df

        """
        # Resource Attributes  na
        Resources main attribute is their count, but will later have volume and
        footprint
        """

        model.resource.attr_na_df
        model.description["Population p"]["Pop Detail pd"]
        model.population.detail_pd_df

        """
        # Population summarized by protection levels pl
        Population main attribute is their count, but will later have things
        like how often they are out doing work and will keep track of things
        like social mobility and columns will have characteristics like age,
        ethnicity, gender as a crosstab.t
        """
        model.population.level_pl_df

    def tables(self, model):
        """Table Exploration.

        Automatically reads from model.description a markdown string
        then displays the data found in the model by traversing the entire
        object looking for Pandas DataFrames
        """
        # https://stackoverflow.com/questions/44790030/return-all-class-variable-values-from-a-python-class
        log = self.log
        log.debug("look for all population items")
        # eventually just go through all the model classes and keep going
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm

        """
        # COVID-19 Data Table Exploration

        Use this section to look through the data. This include the
        descriptions that are included with it.
        """

        # http://net-informations.com/python/iq/instance.htm
        log.debug(f"{model} is {vars(model)}")
        # replaced by iteration
        # for model_value in model:
        # for model_key, model_value in vars(model).items():
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm
        # if issubclass(value, Base):
        #     if isinstance(model_value, Base):
        #         log.debug(
        #          f"object {model_key=} holds {model_value=} subclass of Base"
        #         )
        for base_key, base_value in model:
            # now using the new model iterator that does through all dataframes
            # in a Base class
            for df_name, df_value in base_value:
                # the above replaced these lines
                # for name, value in vars(model_value).items():
                # https://stackoverflow.com/questions/14808945/check-if-variable-is-dataframe
                # if not isinstance(value, pd.DataFrame):
                #     log.debug(f"{value} is not a DataFrame")
                #     continue
                # https://kite.com/python/answers/how-to-check-if-a-value-is-in-a-dictionary-in-python
                # https://www.geeksforgeeks.org/python-check-whether-given-key-already-exists-in-a-dictionary/
                # breakpoint()
                self.write_description(
                    df_name, df_value, base_value.description,
                )
                # if df_name in base_value.description:
                #     log.debug("found description")
                #     st.write(base_value.description[df_name])
                # else:
                #     st.header(df_name)
                #     st.write(f"No description found for {df_name=}")
                # https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
                # https://pbpython.com/styling-pandas.html

    def write_description(
        self, name: str, df: pd.DataFrame, description: Dict
    ):
        """Write Description.

        Writes the description of a nice message if none found
        """
        log = self.log
        if name in description:
            log.debug(f"found {name=} in {description=}")
            st.write(description[name])
            st.write(df.style.format("{0:,.2f}"))
            return
        # st.header(name)
        log.debug(f"No description found for {name=}")

    def test_home(self, data_df):
        """Test drawing.

        Test for dashboard
        """
        log = self.log
        st.write(
            """
            # COVID-19 Decision Dashboard
            ## Restart.us
            Use caution when interpreting these numbers and consult experts on
            use. Numbers are 000s except *$0s*
            """
        )

        log.debug(f"{data_df=}")
        st.write(
            """
            ### All Resource Burn Rate Table
            """
        )

        st.dataframe(data_df.head())
        st.write(
            """
            ### Select Resource for Filtered Burn Rate Table
            """
        )

        # do a multiselect to pick relevant items
        data_ms = st.multiselect(
            "Columns",
            data_df.columns.tolist(),
            default=data_df.columns.tolist(),
        )
        # now render just those columns and the first 10 rows
        filtered_data_df = data_df[data_ms]
        st.dataframe(filtered_data_df.head(10))
        st.write(
            """
            ### Histogram of uses
            """
        )
        # this returns a variable encoding specified with out a type
        reset_df = filtered_data_df.reset_index()
        # https://altair-viz.github.io/user_guide/data.html#long-form-vs-wide-form-data
        st.dataframe(reset_df)
        # ~https://www.geeksforgeeks.org/python-pandas-melt/
        # The melt is basically id_vars are the reset_index
        # the value variables is basically the entire old columns.labels
        wide_df = reset_df.melt(
            id_vars="Level l", value_vars=["N95", "Mask"], value_name="Units"
        )
        st.dataframe(wide_df)
        # https://docs.streamlit.io/en/stable/api.html#display-charts
        st.bar_chart(wide_df)
        # https://altair-viz.github.io/gallery/grouped_bar_chart.html
        chart = (
            alt.Chart(wide_df).mark_bar().encode(x="Resource n:N", y="Units:Q",
                                                 column="Level l:N",
                                                 color="Level l:N")
        )
        st.write(chart)
        # It's so easy to chart with builtin types
        # And labelsa re just more markdown
        st.line_chart(wide_df)

    def visualize_data(self, df, x_axis, y_axis):
        """Visualize data.

        Charting for the dashboard
        """
        # F strings do not work with streamlit so just put variables i
        # so use st.write to get them
        log = self.log
        log.debug(f"{log=}")
        """
        ## Debug
        """
        st.write(f"{x_axis=} {y_axis=}")
        st.write(f"{df.index.name=} {df.columns.name=}")
        st.write(f"{df.index}")
        st.write(f"{df.columns}")
        st.dataframe(df)
        df.index.name = "Label" if None else df.index.name
        # first rest the index to get it to be a column
        # using melt to get column form
        df_reset = df.reset_index()
        st.write(df_reset)
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.melt.html
        # if value_vars are not specified then unpivote everything
        df_melt = df_reset.melt(id_vars=df.index.name, value_name="Units")
        st.write(df_melt)

        # for single values
        # http://scrapingauthority.com/pandas-dataframe-filtering/
        # https://realnitinworks.netlify.app/check-object-iterability.html?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com
        try:
            iter(x_axis)
            df_filter_x = df_melt[df_melt["Level l"].isin(x_axis)]
        except TypeError:
            df_filter_x = df_melt[df_melt["Level l"] == x_axis]
        st.dataframe(df_filter_x)

        try:
            iter(y_axis)
            df_filter_xy = df_filter_x[df_filter_x["Resource n"].isin(y_axis)]
        except TypeError:
            df_filter_xy = df_filter_x[df_filter_x["Resource n"] == y_axis]
        st.dataframe(df_filter_xy)

        # you can also use breakpoint
        # breakpoint()

        # Since this was published, there are more parameters for interactive
        # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
        # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
        # https://altair-viz.github.io
        # https://altair-viz.github.io/user_guide/encoding.html
        graph = (
            alt.Chart(df_melt)
            .mark_bar()
            .encode(x="Level l:N", y="Units:Q")
            .interactive()
        )
        st.write(graph)

        test = pd.DataFrame(
            {"Level l": ["healthcare", "non-healthcare"], "Unit": [22, 123]}
        )
        st.dataframe(test)
        st.write(f"{test=}")
        graph2 = alt.Chart(test).mark_bar().encode(x="Level l", y="Unit")
        st.write(graph2)

    def visualize_model(self, model: Model):
        """Visualize Model.

        Simple visualization
        """
        log = self.log
        log.debug(f"visual {model=}")
        """
        # Model Visualization

        Uses an existing model
        """
        for base_key, base_value in model:
            # now using the new model iterator that does through all dataframes
            # in a Base class. So this assumes the model base data is in
            # ModelData, but the derived data is in all the classes that are in
            # the model
            for df_name, df_value in base_value:
                self.write_description(
                    df_name, df_value, base_value.description
                )
                # breakpoint()
                # self.write_chart(df_name, df_value)

    def write_chart(self, name, df):
        """Write Chart.

        Write out a dataframe as a chart
        """
        log = self.log
        # Get this from wide to narrow form for charting
        indexed_df = df.reset_index()
        index_name = df.index.name
        log.debug(f"{df=}")
        log.debug(f"{df.index.name=}")
        log.debug(f"{df.columns.name=}")
        log.debug(f"{indexed_df=}")
        indexed_df.rename_axis(index=index_name, inplace=True)

        """
        debug
        """
        st.write(name)
        st.write(df)
        st.write(indexed_df)
