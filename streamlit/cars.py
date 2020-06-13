#
# https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
#
# Simple car demonsration

# Standard data sets for demo purposes
from vega_datasets import data

import streamlit as st
import altair as alt


def main():
    df = load_data()
    # Simple selection
    page = st.sidebar.selectbox("Choose page", ["Homepage", "Exploration"])

    if page == "Homepage":
        st.header("Data Explorer")
        st.write("""
Please **select** a page on the left
""")
        st.write(df)
    elif page == "Exploration":
        st.title("Data Exploration")
        x_axis = st.selectbox("Choose x-axis variable", df.columns, index=3)
        y_axis = st.selectbox("Choose y-axis variable", df.columns, index=4)
        visualize_data(df, x_axis, y_axis)


# pragma that says only run this once
@st.cache
def load_data():
    df = data.cars()
    return df


def visualize_data(df, x_axis, y_axis):
    print(df)
    print('x_axis', x_axis)
    print('y_axis', y_axis)
    # Since this was published, there are more parameters for interactive v4
    # https://towardsdatascience.com/quickly-build-and-deploy-an-application-with-streamlit-988ca08c7e83
    # https://towardsdatascience.com/interactive-election-visualisations-with-altair-85c4c3a306f9
    # But the main problem is interactive needs parentheses to pick up the
    # default
    graph = alt.Chart(df).mark_circle(size=60).encode(
        x=x_axis,
        y=y_axis,
        color='Origin',
        tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
        ).interactive()
    st.write(graph)


if __name__ == "__main__":
    main()
