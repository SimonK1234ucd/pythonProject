import pandas as pd
import streamlit as st

def generateChart(dataframe, chart_type):

    chart_type = chart_type.lower()

    charts = ["line", "bar", "scatter", "area", "pie", "table"]

    if dataframe is None:
        st.error("No data to display. Please provide a dataframe to generate the chart.")
        return

    # Checks if the chart type is valid
    if chart_type not in charts:
        st.error("Invalid chart type. Please select a valid chart type.")
        return

    chartString = f"st.{chart_type}_chart(dataframe)"

    return eval(chartString)
