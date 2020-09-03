"""Simple car demonsration.

# https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83

"""
import altair as alt  # type: ignore
import pandas as pd  # type: ignore
import streamlit as st  # type: ignore

# Standard data sets for demo purposes
from vega_datasets import data  # type: ignore


def main():
    """Display main."""
    df = load_data()
    # Simple selection
    page = st.sidebar.selectbox("Choose page", ["Homepage", "Exploration"])

    if page == "Homepage":
        st.header("Data Explorer")
        st.write(
            """
Please **select** a page on the left
"""
        )
        df = pd.DataFrame(
            {"Level l": ["Essential", "Non Essential"], "N95": [123, 23]}
        )
        st.write(df)
        graph = alt.Chart(df).mark_bar().encode(x="Level l", y="N95")
        st.write(graph)

    elif page == "Exploration":
        st.title("Data Exploration")
        x_axis = st.selectbox("Choose x-axis variable", df.columns, index=3)
        y_axis = st.selectbox("Choose y-axis variable", df.columns, index=4)
        visualize_data(df, x_axis, y_axis)


# pragma that says only run this once
@st.cache
def load_data():
    """Get car data."""
    df = data.cars()
    return df


def visualize_data(df, x_axis, y_axis):
    """Show data."""
    print(df)
    print("x_axis", x_axis)
    print("y_axis", y_axis)
    # Since this was published, there are more parameters for interactive v4
    # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
    # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
    # But the main problem is interactive needs parentheses to pick up the
    # default
    graph = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x=x_axis,
            y=y_axis,
            color="Origin",
            tooltip=["Name", "Origin", "Horsepower", "Miles_per_Gallon"],
        )
        .interactive()
    )
    st.write(graph)


if __name__ == "__main__":
    main()
