"""Stock demo.

# vi:se ts=4 sw=4 et:
# Stock demo
# https://towardsdatascience.com/how-to-build-a-data-science-web-app-in-python-61d1bed65020
##
# From https://github.com/restartus/demo-self-driving/blob/master/app.py
# Use a main and a well formed way to run things
#
"""
import streamlit as st  # type: ignore
import yfinance as yf  # type: ignore

# Note how there are no call backs


def main():
    """Display data."""
    # Note that write uses Markdown
    st.write(
        """
# Simple Stock Price Analysis
Shown are the stock **closing price** and ***volume*** of Tesla
    """
    )

    # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
    tickerSymbol = "TSLA"

    tickerData = yf.Ticker(tickerSymbol)
    # Returns a Pandas dataframe
    tickerDf = tickerData.history(
        period="1d", start="2010-05-31", end="2020-06-10"
    )
    print(tickerDf)

    # It's so easy to chart with builtin types
    # And labelsa re just more markdown
    st.write(
        """
    ### Closing Price
    """
    )
    st.line_chart(tickerDf.Close)

    st.write(
        """
    ### Daily Volume
    """
    )
    st.line_chart(tickerDf.Volume)
    # you start this by detecting a magic variable


if __name__ == "__main__":
    main()
