
#
import streamlit as st
import pandas as pd
import numpy as np
# import yfinance as yf
import altair as alt
import logging
from typing import List

# Note how there are no call backs


class Model:
    def __init__(self, name):
        self.name: str = name
        self.label_pop: List[str] = ["healthcare", "Non-healthcare"]
        self.label_resource: List[str] = ["N95 Resp", "N95", "Mask", "Gloves",
                                          "Gowns", "Disinfectant", "Test Kits"]
        self.label_detail: List[str] = ["Landed Cost"]

        # Consumption data
        self.pop_consumption_pn_array = np.array([[1.18, 0.2, 4.51, 6.7, 1.4, 1.5, 0.2],
                                                   [0.1, 0.5, 2.1, 1.0, 0.05, 0.1, 0.01]])
        self.pop_consumption_pn_df = pd.DataFrame(
                                    self.pop_consumption_pn_array,
                                    index=self.label_pop,
                                    columns=self.label_resource)

        # Supply data not you cannot name an member with a 1 so .1n.array does not
        # work
        self.pop_supply_n_array = np.array([4.50, 3.00, 0.5, 0.2, 4.0, 0.45, 4.00])
        self.pop_supply_n_df = pd.DataFrame(self.pop_suppy_n_array,
                                            index=self.label_detail,
                                            columns=self.label_resource)


def main():
    """

    https://towardsdatascience.com/how-to-build-a-data-science-web-app-in-python-61d1bed65020
    Use a main and a well formed way to run things
    https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2
    has more ways to do selects and tables

    """
    # https://docs.python.org/3/howto/logging-cookbook.html
    # logging.basicConfig(level=logging.DEBUG,
    #                     format='%(asctime)s:$(levelname)s:%(message)s')
    # https://stackoverflow.com/questions/56269302/how-to-setup-python-logging-format-using-f-string-style
    # https://docs.python.org/3/howto/logging-cookbook.html
    # note logging does not seem to work at all with streamlit
    logging.basicConfig(level=logging.DEBUG,
                        filename='dashboard.log',
                        style='{',
                        format='{message} ({filename}:{lineno})')
    logging.debug('Start logging')

    logging.debug('model labels and dimensions set')
    model = Model('bharat')

    # https://discuss.streamlit.io/t/editable-data-tables-in-streamlit/529/8
    # hack to edit a table, they do not have editable tables yet
    # Note print here will appear on the web page
    # print('population_consumption_pn_df', population_consumption_pn_df)
    # https://realpython.com/python-f-strings/
    # f"hello world {population_consumption_pn_df}."

    # Simple selection which is the active page
    page = st.sidebar.selectbox("Choose page", ["Homepage", "Exploration"])
    if page == "Homepage":
        homepage(model)
    elif page == "Exploration":
        exploration(model)

    # change global variables
    model.stockpile = st.sidebar.slider('Stockpile (days)',
                                        min_value=0, max_value=180,
                                        value=(30, 90))

    # change costs
    model.costs = st.sidebar.slider('Cost multiplier', min_value=0.0,
                                    max_value=5.0,
                                    value=1.0)


# The home page
def homepage(model):
    st.write("""
    # COVID-19 Decision Dashboard
    ## Restart.us
    Use caution when interpreting these numbers and consult experts on use.
    Numbers are 000s except *$0s*
    """)
    print(population_consumption_pn_df)
    st.write("""
    ### All Resource Burn Rate Table
    """)
    # display the data
    st.dataframe(population_consumption_pn_df.head())
    st.write("""
    ### Select Resource for Filtered Burn Rate Table
    """)
    # do a multiselect to pick relevant items
    data_ms = st.multiselect("Columns",
                             population_consumption_pn_df.columns.tolist(),
                             default=population_consumption_pn_df.columns.tolist())
    # now render just those columns and the first 10 rows
    filtered_population_consumption_pn_df = population_consumption_pn_df[data_ms]
    st.dataframe(filtered_population_consumption_pn_df.head(10))
    st.write("""
    ### Histogram of uses
    """)
    st.bar_chart(filtered_population_consumption_pn_df)
    # It's so easy to chart with builtin types
    # And labelsa re just more markdown
    st.line_chart(population_consumption_pn_df)


def exploration(df):
    print(df)
    st.title("Data Exploration")
    # https://docs.streamlit.io/en/latest/api.html
    x_axis = st.selectbox("Choose x-axis", df.columns, index=0)
    y_axis = st.selectbox("Choose y-axis", df.columns, index=1)
    print('x_axis', x_axis)
    print('y_axis', y_axis)
    # Since this was published, there are more parameters for interactive v4
    # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
    # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
    # https://altair-viz.github.io
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        tooltip=['N95', 'Mask'],
        color='N95'
        ).interactive()
    st.write(graph)


# you start this by detecting a magic variable
if __name__ == "__main__":
    main()
