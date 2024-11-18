# The main.py file is the run, that is actuall run in the brower
# Use streamlit run main.py to start the program.
import streamlit as st
import pandas as pd
import models.getCurrencies as getCurrencies
import altair as alt
import models.getChartMPV as getChartMPV
import models.getreadfile as getreadfile
import models.getPurchasingPower as getPurchasingPower
from models.getreadfile import getcurrencychart
from models.getCurrencyRisk import display_currency_risk
from models.ExchangeSpending import display_spending_comparison
import models.getExpenseByIndex as EXP


# Set the page configuration
st.set_page_config(layout="wide", page_title="Exchange Tool", page_icon="https://seeklogo.com/images/U/university-college-dublin-logo-3AFABC5D8E-seeklogo.com.png")

# Set the page header as a container
headerContainer = st.container()
with headerContainer:
    columns = st.columns(2)
    left = columns[0]
    right = columns[1]

    with left:
        st.markdown("<h1 style='color:deepskyblue;'>Exchange Tool</h1>", unsafe_allow_html=True)
        st.caption("This tool allows you to convert currencies and display exchange rates over time.")

    with right:
        #st.image("https://seeklogo.com/images/U/university-college-dublin-logo-3AFABC5D8E-seeklogo.com.png", width=50)
        st.image("https://i.ibb.co/vjMnKrv/forupload.png[/img][/url]", width=350)

bodyContainer = st.container()
with bodyContainer:
    [currencyInformation, CostofLiving] = st.tabs(["Currency Information","Cost of Living" ])
    with currencyInformation:
    # Create tabs for Currency Converter and Historical Exchange Rates and so on    
        currencyTypes = getCurrencies.getCurrencyTypes().keys() #because of keys just the KEYs is global defined
    # Title of section...
        upper = st.container()
        lower = st.container()

    # ––––––– UPPER SECTION OF THE CURRENCY OVERVIEW TAB –––––––
        with upper:
            [left, right] = st.columns(2)

            # This container is the master configuration for the Currency Overview tab
            # It will allow to changes the metrics of all the graps with one click, gaining insight in that exact currency :).
            with left:

                # Declare default values for the currency overview tab
                initial = 0
                average = 0.02
                years = 100
                time_periods = ["YTD", "1 year", "2 years", "3 years", "5 years", "10 years", "20 years"]

                # Gets the country list for the purchasing power calculator
                listOfCountries = getPurchasingPower.getHistoricalPPlist()
                listOfCurrencies = getreadfile.getAllCurrenciesComparedToEuro()

                # Get the future purchasing power
                forprint = getPurchasingPower.getFuturePP(initial, average ,years)

                # Selected country for the purchasing power calculator
                
                [titleLeft, titleRight] = st.columns(2)
                with titleLeft:
                    selectedCurrency = st.selectbox("Please Select the currency of your interest:", listOfCurrencies, key="tab3c")
                    amount = st.number_input("Enter Amount", value=1, step=1, format="%d", key="amount_input")
                with titleRight:
                    date = st.selectbox("Select Time Period", time_periods, key = "timeperioddate") 

                selectedCurrencies = st.multiselect(
                    "Select Currencies", currencyTypes, default=["USD", "GBP", "JPY"], key="selected_currencies"
                )
                st.caption("The exchange rates are displayed in current time and are subject to change.")

                # Conversion logic
                allCurrencies = getCurrencies.getSpecificCurrency(selectedCurrency)
                rows = []
                headers = ["Base Currency", "Currency", "Exchange Rate", "Amount Exchanged"]

                for currency in selectedCurrencies:
                    exchangeRate = allCurrencies.get(currency, 0)
                    converted_amount = amount * exchangeRate
                    rows.append([f"{amount} {selectedCurrency}", currency, exchangeRate, converted_amount])

                # Display conversion results
                df = pd.DataFrame(rows, columns=headers)
                st.dataframe(df, width=800)
                
            with right:
                # Title of the section
                st.markdown("<p style='font-weight:bold'>Currency Risk Assement</p>", unsafe_allow_html=True)
                display_currency_risk(selectedCurrency)

                st.markdown("<p style='font-weight:bold'>Compare Euro Historically</p>", unsafe_allow_html=True)
                st.markdown("<p style='font-size:14px'>This section provides statistics and graphical information on the historical performance of a selected currency against the Euro.</p>", unsafe_allow_html=True)

                # Set the current date explicitly
                current_date = pd.to_datetime("2024-11-13")

                # Define time periods
                periods = {
                    "YTD": current_date.replace(month=1, day=1),
                    "1 year": current_date - pd.DateOffset(years=1),
                    "2 years": current_date - pd.DateOffset(years=2),
                    "3 years": current_date - pd.DateOffset(years=3),
                    "5 years": current_date - pd.DateOffset(years=5),
                    "10 years": current_date - pd.DateOffset(years=10),
                    "20 years": current_date - pd.DateOffset(years=20),
                }
                start_date = periods.get(date, current_date)

                # Get and filter historical data
                chartplot = getcurrencychart(selectedCurrency)
                chartplot = chartplot[chartplot.index >= start_date]

                # Display the historical chart
                st.write(f"Historical Data of {selectedCurrency} for the Selected Time Period ({date})")
                st.line_chart(chartplot)
                
                    # data3b = getPurchasingPower.getHistorialPPdata(country, years, initial)
                    # st.write(f"The Value of {"{:.2f}".format(initial)} in {years} is {"{:.2f}".format(data3b)}") 


#  Cost of Living Tab –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    with CostofLiving:
        # Changs this to a more correct labelling :)
        # Add content for the Living expenses tab here
        st.markdown("<p style='font-weight:bold'>Overview Cost of Living </p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px'>This tab offers an overview of the cost of living across different countries around the world.</p>", unsafe_allow_html=True)
        #display_spending_comparison()

        [left, right] = st.columns(2)
        
        with left:
            
            [titleLeft, titleRight] = st.columns(2)

            with titleLeft:
                selectedYear = st.selectbox("Select year", [2024, 2023, 2022])

            with titleRight:
                selectedRegion = st.selectbox("Select Region", ["Europe", "Asia", "America", "Africa", "Oceania"])
            
            year = 2024
            region = "Europe"

            if selectedRegion != region:
                region = selectedRegion

            if selectedYear != year:
                year = selectedYear
            dataframe = EXP.getLivingExpenses(year, region)

            availableCountries = [country for country in dataframe["Country"].unique() if country in listOfCountries]
            
            st.caption("The table displays the living costs of different countries indexed in relation to New York (index 100)")
            st.dataframe(dataframe[["Country", "Cost of Living Index", "Rent Index", "Groceries Index", "Restaurant Price Index"]], height=500, width=700)
        
        with right:

            selectedCountry = st.selectbox("Please Select the country of your interest:", availableCountries, key="tab3b")
            [left, right] = st.columns(2)
                    
            with left:
                st.markdown("<p style='font-weight:bold'>Purchasing Power Calculator</p>", unsafe_allow_html=True)
                st.caption("<p style='font-size:14px'>This tab provides comprehensive information for a clear overview of the purchasing power of a selected currency.</p>", unsafe_allow_html=True)
            # Create a radio button for selecting the type of purchasing power
            with right:
                selectedTimeHorizon = st.radio("", ["Historical", "Future"])

            if selectedCountry:
                data3 = getChartMPV.CountryPurchasingPower(selectedCountry)
                st.write(f"Hisorical Money Purchasing Power of {selectedCountry}: ")
                st.line_chart(data3.set_index("Year"))
    