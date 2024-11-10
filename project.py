import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import getCurrencies
import altair as alt


st.set_page_config(layout="wide", page_title="Exchange Tool")

# Use st.markdown to allow HTML with unsafe_allow_html=True

headerContainer = st.container()

with headerContainer:
    columns = st.columns(2)
    left = columns[0]
    right = columns[1]

    with left:
        st.markdown("<h1 style='color:indigo;'>Exchange Tool</h1>", unsafe_allow_html=True)
        st.caption("This tool allows you to convert currencies and display exchange rates over time.")

    with right:
        st.image("https://seeklogo.com/images/U/university-college-dublin-logo-3AFABC5D8E-seeklogo.com.png", width=50)


#Page Layout: 

# Sets up two columns for the page layout
columns = st.columns(2)

# Assigns the left and right columns to variables
leftSide = columns[0]
rightSide = columns[1]

with leftSide:
    # Create tabs for Currency Converter and Historical Exchange Rates
    tabs = st.tabs(["Currency Overview", "Compare Currencies", "Currency Table"])

    currencyTypes = getCurrencies.getCurrencyTypes().keys()

# Add content for the Currency Overview tab here
with tabs[0]:
    st.markdown("<p style='font-weight:bold'>Overview of Currencies</p>", unsafe_allow_html=True)

    # Settings Expander    
    with st.expander("Settings"):
        selectedCur = st.selectbox("Select Currency", currencyTypes)
        
        # Fetch currency list for selected currency
        currencyList = getCurrencies.getSpecificCurrency(selectedCur)
        
        # Convert the currency list to a sorted list of tuples (currency, value)
        sorted_currency_data = sorted(currencyList.items(), key=lambda item: item[1])
        
        # Extract values to calculate thresholds
        values = [value for currency, value in sorted_currency_data]
        min_value = min(values)
        max_value = max(values)
        range_value = max_value - min_value

        # Calculate thresholds based on the range
        interval = range_value / 8
        threshold_options = [(round(min_value + i * interval), round(min_value + (i + 1) * interval)) for i in range(8)]
        
        # Display calculated thresholds in selectbox
        threshold = st.selectbox(
            "Select Threshold",
            options=threshold_options,
            index=0,
            format_func=lambda x: f"{x[0]} - {x[1]}"
        )
        sort_order = st.radio("Sort by Value", ("Ascending", "Descending"))

    valueColumn = f"Value of 1 {selectedCur}"

    # Convert sorted list to a DataFrame
    dataForChart = pd.DataFrame(sorted_currency_data, columns=["Currency", valueColumn])

    # Filter data based on the selected threshold
    filteredData = dataForChart[(dataForChart[valueColumn] >= threshold[0]) & (dataForChart[valueColumn] <= threshold[1])]

    # Sort data based on the selected sort order
    ascending_order = True if sort_order == "Ascending" else False
    filteredData = filteredData.sort_values(by=valueColumn, ascending=ascending_order)

    # Display the filtered and sorted bar chart
    chart = alt.Chart(filteredData).mark_bar().encode(
        x=alt.X("Currency", sort=None),
        y=valueColumn
    ).properties(height=400, width=550)

    st.altair_chart(chart)

    # Add content for the Overview tab here
    with tabs[1]:
        

        st.markdown("<p style='font-weight:bold'>Currency Converter</p>", unsafe_allow_html=True)
        # Add content for the Currency Converter tab here
        
        selectedCurrencies = st.multiselect("Select Currencies", currencyTypes, default=["USD", "EUR"],)

        for cur in selectedCurrencies:

            st.write(f"100 USD = {currencyList[cur]*100} {cur}")

    # Add content for the Currency Table tab here
    with tabs[2]:
        st.markdown("<p style='font-weight:bold'>Currency Table</p>", unsafe_allow_html=True)
        currency_df = pd.DataFrame(list(currencyList.items()), columns=["Currency", "Value of 1 USD"])
        st.dataframe(currency_df, width=500, height=500)
        

# Add any additional content you need on the right side
with rightSide:
    tabs = st.tabs(["Grocery Checker", "Buying Power Overview"])

    # Add content for the Grocery Checker tab here
    with tabs[0]:
        st.markdown("<p style='font-weight:bold'>Grocery Checker</p>", unsafe_allow_html=True)
        # Add content for the Grocery Checker tab here

    # Add content for the Buying Power Overview tab here
    with tabs[1]:
        st.markdown("<p style='font-weight:bold'>Buying Power Overview</p>", unsafe_allow_html=True)
        # Add content for the Buying Power Overview tab here
    
    
    # Add content for the right column


#Splitter for the page layout
st.empty()