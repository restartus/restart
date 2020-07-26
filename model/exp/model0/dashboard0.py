"""Stock demo.

# vi:se ts=4 sw=4 et:
# Stock demo
# https://towardsdatascience.com/how-to-build-a-data-science-web-app-in-python-61d1bed65020
##
# From https://github.com/restartus/demo-self-driving/blob/master/app.py
# Use a main and a well formed way to run things
#
# https://towardsdatascience.com/streamlit-101-an-in-depth-introduction-fc8aad9492f2
# has more ways to do selects and tables
#
"""
# import yfinance as yf
# import model as md
import altair as alt  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st  # type: ignore

# Note how there are no call backs


def main():
    """Set sample test data."""
    data_df = pd.DataFrame(
        [[0, 123], [12, 23]],
        index=["healthcare", "Non-healthcare"],
        columns=["N95", "Mask"],
    )

    # Simple selection
    page = st.sidebar.selectbox("Choose page", ["Homepage", "Exploration"])
    if page == "Homepage":
        homepage(data_df)
    elif page == "Exploration":
        st.title("Data Exploration")
        # https://docs.streamlit.io/en/latest/api.html
        x_axis = st.selectbox("Choose x-axis", data_df.columns, index=0)
        y_axis = st.selectbox("Choose y-axis", data_df.columns, index=1)
        visualize_data(data_df, x_axis, y_axis)
    # Not that write uses Markdown


# The home page
def homepage(data_df):
    """Show Homepage."""
    st.write(
        """
    # COVID-19 Decision Dashboard
    ## Restart.us
    Use caution when interpreting these numbers and consult experts on use.
    Numbers are 000s except *$0s*
    """
    )
    print(data_df)
    st.write(
        """
    ### All Resource Burn Rate Table
    """
    )
    # display the data
    st.dataframe(data_df.head())
    st.write(
        """
    ### Select Resource for Filtered Burn Rate Table
    """
    )
    # do a multiselect to pick relevant items
    data_ms = st.multiselect(
        "Columns", data_df.columns.tolist(), default=data_df.columns.tolist()
    )
    # now render just those columns and the first 10 rows
    filtered_data_df = data_df[data_ms]
    st.dataframe(filtered_data_df.head(10))
    st.write(
        """
    ### Histogram of uses
    """
    )
    st.bar_chart(filtered_data_df)
    # It's so easy to chart with builtin types
    # And labelsa re just more markdown
    st.line_chart(data_df)


def visualize_data(df, x_axis, y_axis):
    """Visualize data."""
    print(df)
    print("x_axis", x_axis)
    print("y_axis", y_axis)
    # Since this was published, there are more parameters for interactive v4
    # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
    # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
    # https://altair-viz.github.io
    graph = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(x=x_axis, y=y_axis, tooltip=["N95", "Mask"], color="N95")
        .interactive()
    )
    st.write(graph)


# you start this by detecting a magic variable
if __name__ == "__main__":
    main()
