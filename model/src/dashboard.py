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
        # TODO: Put all this stuff into a library
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
                "Home",
                "Tables",
                "Exploration",
                "Test Home",
                "Test Tables",
                "Test Exploration",
            ],
        )

        inv_min_in_periods = st.sidebar.slider(
            "Stockpile", max_value=120, value=30, step=15,
        )
        log.debug(f"{inv_min_in_periods=}")

        self.debug_level = st.sidebar.slider(
            "Debug (0=no debug output, 100=massive output) ", value=0
        )
        # the logging level is the reverse sense,
        # it is the supression level
        # if you want 90% of the messages set logging.DEBUG is 10
        # if you want 20 of the messages set logging.CRITICAL is 80
        self.debug_level = 100 - self.debug_level
        if self.debug_level <= logging.DEBUG:
            st.sidebar.markdown(f"{self.debug_level=}")

        # To make this work for the update, use up all the exiting inventory
        model.resource.demand(model.resource.inventory_ln_df)
        model.resource.set_inv_min(
            model.demand.level_total_demand_ln_df, inv_min_in_periods
        )

        if self.page == "Home":
            self.home_page(model)
        elif self.page == "Tables":
            self.tables_page(model)
        elif self.page == "Exploration":
            self.exploration_page(model)
        elif self.page == "Test Tables":
            self.test_tables_page(model)
        elif self.page == "Test Home":
            self.test_home_page(self.data_df)
        elif self.page == "Test Exploration":
            self.test_exploration_page()

    def test_exploration_page(self):
        """Testing Exploration Options."""
        st.title("Data Exploration")
        # https://docs.streamlit.io/en/latest/api.html
        st.dataframe(self.data_df)
        if self.debug_level <= logging.DEBUG:
            st.write(f"{self.data_df.index=}")
            st.write(f"{self.data_df.columns=}")
        x_axis = st.selectbox("Choose x-axis", self.data_df.index, index=0)
        y_axis = st.selectbox("Choose y-axis", self.data_df.columns, index=1)
        if self.debug_level <= logging.DEBUG:
            st.write(f"{x_axis=} {y_axis=}")
        x_multi = st.multiselect("Select Summary Levels", self.data_df.index)
        y_multi = st.multiselect(
            "Select Resource to Display", self.data_df.columns
        )
        if self.debug_level <= logging.DEBUG:
            st.write(f"{x_multi=}")
            st.write(f"{y_multi=}")
        self.visualize_data(self.data_df, x=x_axis, y=y_axis)
        self.visualize_data(self.data_df, x=x_multi, y=y_multi)
        # Not that write uses Markdown
        self.test_graph()

    def home_page(self, model):
        """Home page."""
        st.markdown(
            """
        # COVID-19 Decision Dashboard Stockpile Analysis
        ## Restart.us

        To use the surge model, change the slider for stockpile days on the
        right and the table below will change to indicate minimum inventory
        required.

        Use caution when interpreting these numbers
        """
        )
        # this will change based on the stockpile
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
        # none of these work in streamlit
        # pd.set_option("display.precision", 0)
        # pd.set_option("display.float_format", "{:,.0f}".format)
        # pd.options.display.float_format = "{:,.0f}".format
        # https://stackoverflow.com/questions/43102734/format-a-number-with-commas-to-separate-thousands-in-python
        # https://mkaz.blog/code/python-string-format-cookbook/
        st.write(model.resource.inventory_ln_df.style.format("{:,.0f}"))
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html
        self.visualize_data(model.resource.inventory_ln_df)

    # uses the literal magic in Streamlit 0.62
    # note that just putting an expression automatically wraps an st.write
    def test_tables_page(self, model):
        """Tables.

        The full graphical display of all tables use for debugging mainly
        """
        st.write(
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

        ## Resource safety Stock ln.

        The supply of resource needs in model.resource.inv_min_rln_df
        """
        )
        st.write(model.resource.inv_min_rln_df)

        st.write(
            """
        ## Resource Attributes na
        Resources main attribute is their count, but will later have volume and
        footprint

        In model.resource.attr_na_df
        """
        )

        st.write(model.resource.attr_na_df)

        st.write(
            """
        # The Descriptions

        in model.config["Description"]
        """
        )
        st.write(
            model.config["Description"]["Population p"]["Pop Detail pd"].get()
        )

        st.write(
            """
        ## The population details

        In model.population.detail_pd_df

        """
        )
        st.write(model.population.detail_pd_df)

        st.write(
            """
        # Population summarized by protection levels pl
        Population main attribute is their count, but will later have things
        like how often they are out doing work and will keep track of things
        like social mobility and columns will have characteristics like age,
        ethnicity, gender as a crosstab.t
        """
        )
        st.write(model.demand.level_pl_df)

    def tables_page(self, model):
        """Table Exploration.

        Automatically reads from model.description a markdown string
        then displays the data found in the model by traversing the entire
        object looking for Pandas DataFrames
        """
        # https://stackoverflow.com/questions/44790030/return-all-class-variable-values-from-a-python-class
        log = self.log
        log.debug("look for all population items")
        if self.debug_level <= logging.DEBUG:
            st.write(f"in tables page on {model=}")
        # eventually just go through all the model classes and keep going
        # http://effbot.org/pyfaq/how-do-i-check-if-an-object-is-an-instance-of-a-given-class-or-of-a-subclass-of-it.htm

        st.write(
            """
        # COVID-19 Data Table Exploration

        Use this section to look through the data. This include the
        descriptions that are included with it.
        """
        )

        # http://net-informations.com/python/iq/instance.htm
        log.debug(f"{model=} is {vars(model)=}")
        if self.debug_level <= logging.DEBUG:
            st.write(f"{model=} is {vars(model)=}")
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
        log.debug(f"{name=}")
        if self.debug_level <= logging.DEBUG:
            st.write("in write_description")
            st.write(f"{name=}")

        if name in description:
            log.debug(f"found {name=} in {description=}")
            st.write(description[name])
            # this style fails could be streamlit bug
            # only fails for the first item population details
            # st.dataframe(df.style.format("{:,.0f}"))
            st.dataframe(df)
            return
        # st.header(name)
        log.debug(f"No description found for {name=}")
        st.write(
            f"""
            ## {name} Has No Description
            No description in found for {name=}
            """
        )
        if self.debug_level <= logging.ERROR:
            st.write(f"Missing in {description=}")

    def test_home_page(self, data_df):
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
            alt.Chart(wide_df)
            .mark_bar()
            .encode(
                x="Resource n:N",
                y="Units:Q",
                column="Level l:N",
                color="Level l:N",
            )
        )
        st.write(chart)
        # It's so easy to chart with builtin types
        # And labelsa re just more markdown
        st.line_chart(wide_df)

    def visualize_data(self, df, x=None, y=None):
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
        if self.debug_level <= logging.DEBUG:
            st.write(f"{x=} {y=}")
            st.write(f"{df.index.name=} {df.columns.name=}")
            st.write(f"{df.index=}")
            st.write(f"{df.columns=}")
            st.dataframe(df)
        df.index.name = "Label" if None else df.index.name
        # first reset the index to get it to be a column
        # using melt to get column form
        df_reset = df.reset_index()
        if self.debug_level <= logging.DEBUG:
            st.write(df_reset)
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.melt.html
        # if value_vars are not specified then unpivote everything
        # Note Units is used already, so need a different name
        df_melt = df_reset.melt(id_vars=df.index.name, value_name="Count")
        if self.debug_level <= logging.DEBUG:
            st.write(df_melt)

        # for single values
        # http://scrapingauthority.com/pandas-dataframe-filtering/
        # https://realnitinworks.netlify.app/check-object-iterability.html?utm_campaign=News&utm_medium=Community&utm_source=DataCamp.com

        # TODO: implement filtering
        # df_filter_x = df_melt[df_melt[df.index.name].isin(x)]
        # st.dataframe(df_filter_x)
        # try:
        #  iter(y_axis)
        # df_filter_xy = df_filter_x[df_filter_x[df.columns.name].isin(y_axis)]
        # except TypeError:
        # df_filter_xy = df_filter_x[df_filter_x[df.columns.name] == y_axis]
        # df_filter_xy = df_filter_x[df_filter_x[df.columns.name].isin(y)]
        # st.dataframe(df_filter_xy)

        # Since this was published, there are more parameters for interactive
        # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
        # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
        # https://altair-viz.github.io/user_guide/encoding.html
        mapping = [
            ["x", alt.X],
            ["column", alt.Column],
            ["color", alt.Color],
            ["size", alt.Size],
        ]
        # make the Y axis the last column which in narrow form is always
        # the data
        y = df_melt.columns[-1]
        y_alt = y + ":Q"
        encoding = {"y": alt.Y(y_alt)}

        for col in range(0, df_melt.shape[1] - 1):
            var = df_melt.columns[col]
            # tricky, but add to the encoding dictionary
            # using the first item which is a string
            # Then the second is the function in Altair
            # to be called with which creates the right object
            encoding[mapping[col][0]] = mapping[col][1](var + ":N")
        if self.debug_level <= logging.DEBUG:
            st.write(f"{encoding=}")
        chart = alt.Chart(df_melt, encoding=encoding).mark_bar()
        st.write(chart)

        if self.debug_level <= logging.DEBUG:
            st.write(f"{encoding=}")
            self.test_encode(df_melt)

    def test_encode(self, df_melt):
        """Test dynamic encoding for Altair."""
        # Using the constructor interface
        # https://altair-viz.github.io/user_guide/internals.html
        st.write("test_encode")
        width = df_melt.shape[1]
        st.write(f"{width=}")
        st.write(f"{df_melt.columns=}")
        y = df_melt.columns[-1]
        y_alt = y + ":Q"
        encoding = {"y": alt.Y(y_alt)}
        # Now progressively assign the wider we go
        # This is easy for users, but hard to crate this
        # automatically, encode looks like it i really a ditionary
        # passed as **kwargs
        if width >= 2:
            x = df_melt.columns[0]
            x_alt = x + ":N"
            encoding["x"] = alt.X(x_alt)
        if width >= 3:
            column = df_melt.columns[1]
            column_alt = column + ":N"
            encoding["column"] = alt.Column(column_alt)
        if width >= 4:
            color = df_melt.columns[2]
            color_alt = color + ":N"
            encoding["color"] = alt.Color(color_alt)
        st.write(f"{encoding=}")
        dict_graph = alt.Chart(df_melt, encoding=encoding).mark_bar()
        st.write(dict_graph)
        graph = (
            alt.Chart(df_melt)
            .mark_bar()
            # .encode(x="Level l:N", y="Units:Q")
            .encode(x=x_alt, y=y_alt, column=column_alt)
            .interactive()
        )
        st.write(graph)
        test_graph = alt.Chart(
            df_melt,
            mark="bar",
            encoding=alt.FacetedEncoding(
                x=alt.PositionFieldDef(field=x, type="nominal"),
                y=alt.PositionFieldDef(field=y, type="quantitative"),
            ),
        )
        st.write(test_graph)
        # using a dictionary to pass to encode
        # https://altair-viz.github.io/user_guide/encoding.html
        # this only works for 3 wides
        if width < 3:
            return
        encode = dict(
            x=alt.X(x_alt), y=alt.Y(y_alt), column=alt.Column(column_alt)
        )
        st.write(f"{encode=}")
        encode_graph = alt.Chart(df_melt, mark="bar", encoding=encode)
        st.write(encode_graph)
        # test adding dynamically to dictionary
        encode2 = {}
        encode2["x"] = alt.X(x_alt)
        encode2["y"] = alt.Y(y_alt)
        encode2["column"] = alt.Column(column_alt)
        st.write(f"{encode2=}")
        encode2_graph = alt.Chart(df_melt, encoding=encode2).mark_bar()
        st.write(encode2_graph)

    def test_graph(self):
        """Test graphing."""
        test = pd.DataFrame(
            {"Level l": ["healthcare", "non-healthcare"], "Unit": [22, 123]}
        )
        st.dataframe(test)
        st.write(f"{test=}")
        graph2 = alt.Chart(test).mark_bar().encode(x="Level l", y="Unit")
        st.write(graph2)

    def exploration_page(self, model: Model):
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
                self.visualize_data(df_value)

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
