# Import necessary libraries and modules
# Streamlit is used for creating the web app interface.
# Pandas is used for data manipulation and analysis.
# Models and other utilities are imported for handling specific functionalities like fetching data and creating charts.
import streamlit as st
import pandas as pd
import models.getCurrencies as getCurrencies
import altair as alt
import models.getChartMPV as getChartMPV
import models.getreadfile as getreadfile
import models.getPurchasingPower as getPurchasingPower
from models.getreadfile import getAllCurrenciesComparedToEuro, getspecificdatedata, getcurrencychart
from models.getCurrencyRisk import display_currency_risk
from models.ExchangeSpending import display_spending_comparison
import models.getExpenseByIndex as EXP
import models.getExchangeCalculator as ESC

# Configure the Streamlit page
# This sets up a wide layout, a custom title, and an icon for the web app.
st.set_page_config(
    layout="wide",
    page_title="Exchange Tool",
    page_icon="https://seeklogo.com/images/U/university-college-dublin-logo-3AFABC5D8E-seeklogo.com.png"
)

# Page Header Section
# Displays the title and description of the Exchange Tool application
headerContainer = st.container()
with headerContainer:
    columns = st.columns(2)
    left = columns[0]
    right = columns[1]

    # Left column: App title and caption
    with left:
        st.markdown("<h1 style='color:deepskyblue;'>Exchange Tool</h1>", unsafe_allow_html=True)
        st.caption("This tool allows you to convert currencies and display exchange rates over time.")

    # Right column: App logo
    with right:
        st.image("https://i.ibb.co/vjMnKrv/forupload.png", width=350)

# Body Container for Main Tabs
# Contains two main sections: Currency Information and Cost of Living
bodyContainer = st.container()
with bodyContainer:
    [currencyInformation, CostofLiving] = st.tabs(["Currency Information", "Cost of Living"])

    # Currency Information Section
    with currencyInformation:
        # Sub-tabs for various currency-related tools
        [currenOverviewTab, compareCurrenciesTab, currenciesHistoricallyTab, purchasingPowerTab] = st.tabs(["Currency Overview", "Compare Currencies", "Currencies Historically", "Purchasing Power Calculator"])
         
        # Fetch all available currency types
        currencyTypes = getCurrencies.getCurrencyTypes().keys()

        # Currency Overview Tab
        with currenOverviewTab:
            # Display description and functionality for currency overview
            st.markdown("<p style='font-weight:bold'>Overview of Currencies</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>The Currency Overview displays the Exchange Rate of a selected currency compared to other currencies.</p>", unsafe_allow_html=True)
   
            [left, empty, empty2, right] = st.columns(4)

            # Right column: Currency selection and sorting options
            with right:
                selectedCur = st.selectbox("Select Currency", currencyTypes)
                sort = st.radio("Sort by Exchange Rate", ("Ascending", "Descending"))

                # Fetch and sort currency data for the selected currency
                currencyList = getCurrencies.getSpecificCurrency(selectedCur)
                sorted_currency_data = sorted(currencyList.items(), key=lambda item: item[1])
                
                # Calculate thresholds for filtering
                values = [value for currency, value in sorted_currency_data]
                median = pd.Series(values).median()
                minValue = 1
                maxValue = median + 50
                threshold = (minValue, maxValue)

            # Create a DataFrame for charting
            valueColumn = f"Exchange Rate"
            dataForChart = pd.DataFrame(sorted_currency_data, columns=["Currency", valueColumn])
            filteredData = dataForChart[(dataForChart[valueColumn] >= threshold[0]) & (dataForChart[valueColumn] <= threshold[1])]

            # Sort data based on user selection
            ascending_order = True if sort == "Ascending" else False
            filteredData = filteredData.sort_values(by=valueColumn, ascending=ascending_order)

            # Left column: Display bar chart
            with left:
                chart = alt.Chart(filteredData).mark_bar().encode(
                    x=alt.X("Currency", sort=None),
                    y=valueColumn
                ).properties(height=600, width=900)

                st.altair_chart(chart)

        # Compare Currencies Tab
        with compareCurrenciesTab:
            # Displays currency conversion tool for user-selected currencies
            st.markdown("<p style='font-weight:bold'>Currency Converter</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>The Currency Converter transforms a selected currency into other specified currencies.</p>", unsafe_allow_html=True)

            [left, right] = st.columns(2)
            
            with left:
                baseCurrency = st.selectbox("Select Base Currency", currencyTypes)
            with right:
                amount = st.number_input("Enter Amount", value=1, step=1, format="%d")

            allCurrencies = getCurrencies.getSpecificCurrency(baseCurrency)
            selectedCurrencies = st.multiselect("Select Currencies", currencyTypes, default=["USD", "GBP", "JPY"])

            # Generate table for converted amounts
            rows = []
            headers = ["Base Currency", "Currency", "Exchange Rate", "Amount Exchanged"]
            for currency in selectedCurrencies:
                selectedAmountExchangeRated = amount * allCurrencies[currency]
                rows.append([f"{amount} {baseCurrency}", currency, allCurrencies[currency], selectedAmountExchangeRated])

            df = pd.DataFrame(rows, columns=headers)
            st.dataframe(df, width=1250)
            st.bar_chart(df.set_index("Currency")["Exchange Rate"], height=250)

        # Add similar comments for other tabs such as Currencies Historically, Purchasing Power Calculator, and Cost of Living
