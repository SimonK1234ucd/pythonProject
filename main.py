# The main.py file is the run, that is actuall run in the brower
# Use streamlit run main.py to start the program.
import streamlit as st
import pandas as pd
import models.getCurrencies as getCurrencies
import altair as alt
import models.getChartMPV as getChartMPV
import models.getreadfile as getreadfile
import models.getPurchasingPower as getPurchasingPower
from models.getreadfile import getAllCurrenciesComparedToEuro, getspecificdatedata, getcurrencychart
from models.getCurrencyRisk import display_currency_risk
#from models.ExchangeSpending import display_spending_comparison
#import models.generateChart as gc
import models.getExpenseByIndex as EXP
import models.getExchangeCalculator as ESC

# Change page configuration to other settings than default
st.set_page_config(layout="wide", page_title="Exchange Tool", page_icon="https://seeklogo.com/images/U/university-college-dublin-logo-3AFABC5D8E-seeklogo.com.png")

# defining a headerConatiners, which holds the header of the page
headerContainer = st.container()

# with = "in the container put" 
with headerContainer:
    # Creating two columns and assigning each column to a variable by index...
    [left, right] = st.columns(2)

    with left: # Adding markdown to the left column
        st.markdown("<h1 style='color:deepskyblue;'>Exchange Tool</h1>", unsafe_allow_html=True)
        st.caption("This tool enables you to convert currencies, access detailed statistics, explore cost of living information, and much more.")

    with right: # Adding an image to the right column of UCD and group names...
        st.image("https://i.ibb.co/vjMnKrv/forupload.png[/img][/url]", width=350)

bodyContainer = st.container() # Define body container to group elements

with bodyContainer:
    # Defines two tabs and assigns it by index
        # These are the two overall tabs for the page...
    [currencyInformation, CostofLiving] = st.tabs(["Currency Information","Cost of Living" ])

    # With the first of the two tabs, we can now add content to the tab...
    with currencyInformation:
        # Create tabs for Currency Converter and Historical Exchange Rates and so on
        tabs = st.tabs(["Currency Overview", "Compare Currencies", "Currencies Historically", "Purchasing Power Calculator"])
        # Assign each tab to a variable by index
        currenOverviewTab = tabs[0]
        compareCurrenciesTab = tabs[1]
        currenciesHistoricallyTab = tabs[2]
        purchasingPowerTab = tabs[3]
        
        # Get the keys the currency types, which are the abbreviations of the currencies e.g. USD, EUR, JPY etc...
        currencyTypes = getCurrencies.getCurrencyTypes().keys() 

        # Add content for the Currency Overview tab here
        with currenOverviewTab:
            st.markdown("<p style='font-weight:bold'>Overview of Currencies</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>The Currency Overview displays the Exchange Rate of a selected currency compared to other currencies.</p>", unsafe_allow_html=True)
   
            #A dropdown for selecting the currency
            selectedCur = st.selectbox("Select Currency", currencyTypes)

            # Fetch currency list for selected currency
            currencyList = getCurrencies.getSpecificCurrency(selectedCur)
            
            # Convert the currency list to a sorted list of tuples (currency, value)
            sorted_currency_data = sorted(currencyList.items(), key=lambda item: item[1])
        
            # Extract values to calculate thresholds
            values = list(map(lambda item: item[1], sorted_currency_data)) # declares as list, by mapping each tuplet to the second value of the tuple, which is the value of the currency
            median = pd.Series(values).median() # Gets the median to set the threshold accordingly
            minValue= 1
            maxValue= median +50

            threshold =(minValue, maxValue)
                
            # Create a bar chart for the selected currency
            valueColumn = f"Exchange Rate"

            # Convert sorted list to a DataFrame
            dataForChart = pd.DataFrame(sorted_currency_data, columns=["Currency", valueColumn])

            # Filter data based on the selected threshold
            filteredData=dataForChart[(dataForChart[valueColumn] >= threshold[0]) & (dataForChart[valueColumn] <= threshold[1])]# select the date where the value of dataforchart is in given threshold
            st.write(f"This chart displays the exchange rate of the {selectedCur} against the listed currencies:")
            sorted_data = filteredData.sort_values(by=valueColumn)
            st.bar_chart(data=sorted_data,x="Currency",y=valueColumn,height=500)
            
                     
        # Add content for the Compare Currencies tab here
        with compareCurrenciesTab:
            st.markdown("<p style='font-weight:bold'>Currency Converter</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>The Currency Converter transforms a selected currency into other specified currencies.</p>", unsafe_allow_html=True)

            # Create two columns for side-by-side selection boxes
            [left, right] = st.columns(2)        
            #get the base currency and then create the currenylist for this currency
            

            with left:
                # In the left column, we create a selection box for the base currency
                baseCurrency = st.selectbox("Select Base currency",currencyTypes) # e.g. EUR

            with right:
                # Default amount is 1
                amount=1
                # In the right column, we create a number input for the amount of the base currency
                amountInput = st.number_input("Enter Amount", value=1, step=1, format="%d") #amount of base currency#   %d-> user only can put in whole values 1,2,3,
                if amountInput <= 0:
                    st.error("Please provide amount bigger than 0")
                else:
                    amount = amountInput
                
            #select here the currency the user like to convert to             
            allCurrencies = getCurrencies.getSpecificCurrency(baseCurrency) #gets the other currencies in relation to the selected currency (basecurrency)
            
            selectedCurrencies= st.multiselect("Select Currencies", currencyTypes, default=[ "USD","GBP", "JPY"],)  #Multiselect to include multiple currencies to compare to

            st.caption("The exchange rates are displayed in current time and are subject to change.")

            # Empy list for the rows, which will be used to create the DataFrame
            rows = []
            # Defining the headers for the table
            headers = ["Base Currency Value", "Currency", "Exchange Rate", "Amount Exchanged"] #for table headers

            # We iterate over the selected currencies and calculate the amount exchanged for each currency
            for currency in selectedCurrencies:
                
                selectedAmountExchangeRated = amount * allCurrencies[currency] #calculating the amount exchanged
                selectedAmountBaseCurrency = f"{amount} {baseCurrency}" # generates a string of the amount and the base currency (to clearly display the amount)
                exchangeRateForSingleBaseCurrency = allCurrencies[currency] # gets the single exchange rate for the selected currency

                rows.append([selectedAmountBaseCurrency, currency, exchangeRateForSingleBaseCurrency, selectedAmountExchangeRated])#adding these values to the rows list

            # Create a DataFrame from the rows
            df = pd.DataFrame(rows, columns=headers) #create dataframe for table
            
            # Display the table and the bar chart
            st.dataframe(df, width=1250) #create table
            st.caption("The table displays the amount of the base currency exchanged to the selected currencies.") # Short caption to explain the table

            st.bar_chart(df.set_index("Currency")["Exchange Rate"], height=250)
            st.caption(f"The bar chart displays the exchange rate of the {baseCurrency} against the selected currencies.") # Short caption to explain the chart
                 
            
        with currenciesHistoricallyTab: # Everything in the Historical Exchange Rates tab

            st.markdown("<p style='font-weight:bold'>Compare Euro Historically</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab offers statistics and graphical information on the historical performance of a selected currency against the Euro.</p>", unsafe_allow_html=True)

            # Get the list of all the currencies against the euro
            currencylistE = getreadfile.getAllCurrenciesComparedToEuro()

            # Create two columns for side-by-side selection boxes
            [left, right] = st.columns(2)

            with left:
                curE = st.selectbox("Select Currency to Compare", currencylistE, key = "tab2a") # Selected currency for the comparison

            time_periods = ["YTD", "1 year", "2 years", "3 years", "5 years", "10 years", "20 years"] # List of available time periods

            with right:
                selectedDate = st.selectbox("Select Time Period", time_periods, key = "time_period")  # Dropdown for selecting time period
            
            # Set the current date
            current_date = pd.to_datetime("2024-11-13")

            
            periods = { # Dictionary of start dates, where the key is the time period and the value is the start date
                "YTD": current_date.replace(month = 1, day = 1), # Replaces the month and day of the current date with 1, to get the beginning of the year (YTD)
                "1 year": current_date - pd.DateOffset(years=1), # current date -1 year
                "2 years": current_date - pd.DateOffset(years=2),
                "3 years": current_date - pd.DateOffset(years=3),
                "5 years": current_date - pd.DateOffset(years=5),
                "10 years": current_date - pd.DateOffset(years=10),
                "20 years": current_date - pd.DateOffset(years=20),
            }
            # Defines start date as 
            start_date = periods.get(selectedDate, current_date) #when selection of timeframe matches on period in dictionary, this one gets returned (default=current date)

            # Get the historical chart data for the selected currency
            chartplot = getcurrencychart(curE)

            # Filter the data based on the selected time period
            chartplot = chartplot[chartplot.index >= start_date] # This filters the DataFrame chartplot by selecting only the rows where the index satisfies the condition.

            # Short caption to explain the chart
            st.write(f"Historical Data of the Exchange Rate of the {curE} against the EUR for the Selected Time Period ({selectedDate})")
            
            #Plots the chart as a line chart
            st.line_chart(chartplot, height=250)
            
            # Display currency risk assessment
            st.markdown("<p style='font-weight:bold; font-size:22px'>Currency Risk Assessment:</p>", unsafe_allow_html=True)
            display_currency_risk(curE,start_date) # Calls the display_risk_function that returns a chart of the currency risk

        with purchasingPowerTab:

            st.markdown("<p style='font-weight:bold'>Purchasing Power Calculator</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab provides comprehensive information for a clear overview of the purchasing power of a selected currency.</p>", unsafe_allow_html=True)
        
            [historical,future] = st.columns(2)

            with future:
                st.write("Future Purchasing Power Calulator")
            
                with st.expander("Future PPC Configuration"): #
                    
                    #provide and error-test initial input
                    initial=0
                    initialinput=st.number_input("Provide Initial Amount in EUR")
                    if initialinput<0:
                        st.error("Please provide initial input bigger than 0")
                    else:
                        initial=initialinput

                    #provide and error-test inflation input
                    average=0
                    inflationinput=st.number_input("Provide Average Inflation Rate in %  (max. +/- 20%)")
                    if inflationinput<-20 or inflationinput>20:
                        st.error("Please provide initial input in given range ")
                    else:
                        average=inflationinput

                    #provide and error-test year input
                    years=0
                    yearsinput=st.number_input("Provide Amount of Years  (max. 100)")
                    if yearsinput<0:
                        st.error("Please provide initial input bigger than 0")
                    else:
                        years=yearsinput

                if years and initial and average!=0:
                    forprint=getPurchasingPower.getFuturePP(initial,average,years)#gets the future Purchasing Power ready to print
                    st.info(forprint)

            
            with historical:
                st.write("Historical Purchasing Power Calulator") # Small title for the historical Purchasing Power Calculator

                with st.expander("Historical PPC Configuration"): # Declare an expander to hide the configuration options

                    listcountrys = getPurchasingPower.getHistoricalPPlist() # Calls getHistoricalPPlist to get the list of available countries
                    country = st.selectbox("Please Select the country of your interest:", listcountrys, key="tab3b") #Populates a selection box with the retrieved contries
                    
                    # Provide inital amount and errror check it 
                    initialinput = float(st.number_input(f"Amount")) # User input for the initial amount makes sure it is a float
                    st.caption("Please provide the amount you would like to examine") # caption for clarification

                    if initialinput < 0: # Error check for the initial amount is less than zero aka. negative...
                        st.error("Amount must be greater than 0") # Error message if the amount is less than zero
                    
                    availableYears = sorted([str(year) for year in range(1970, 2024)], reverse = True) # A loop with a range of years from 1970 to 2024, which is then sorted in reverse order
                    years = st.selectbox("Please Select the year of your interest:", availableYears, key="tab3c") # Selection box for the year of interest
                    
                    # Error checks for the country and year
                    if country is None: # Error check for the country is None
                        st.error("Please select a country") # Error message if the country is None

                    if years is None: # Error check for the year is None
                        st.error("Please select a year") # Error message if the year is None

                    data3 = getChartMPV.CountryPurchasingPower(country) # Retrieves a dataframe from the CountryPurchasingPower function from the getChartMPV module
                    st.write(f"Hisorical Money Value of {country}: (Index scaled: 100 = 1970)")

                # Indented back to the same level as the with historical: to ensure the chart is displayed in the same column as the historical Purchasing Power Calculator               
                st.line_chart(data3.set_index("Year"))#data3.set_index("Year") converts Year column in index – ensures using Year as x-Achsi 
   
                data3b = getPurchasingPower.getHistorialPPdata(country, years, initialinput) #to get historical data 
                
                if initialinput != 0:
                    st.info(f"The Purchasing Power of {"{:.2f}".format(initialinput)} today is equal to {"{:.2f}".format(data3b)} in {years}")            
                elif initialinput == 0: # Error check for the initial amount is zero
                    st.info("Please provide an amount in order to proceed")

                
            

    with CostofLiving:
            # Changs this to a more correct labelling :)
        tabs = st.tabs(["Cost of Living Overview","Exchange Spending Calculator"])
        CoLOverview = tabs[0]
        exchaangespendigcalc = tabs[1]
        
        # Add content for the Living expenses tab here
        with CoLOverview:
            st.markdown("<p style='font-weight:bold'>Overview Cost of Living </p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab offers an overview of the cost of living across different countries around the world.</p>", unsafe_allow_html=True)

            selectWrapper = st.container()
            with selectWrapper:

                columns = st.columns(2)

                with columns[0]:
                    selectedYear = st.selectbox("Select year", [2024, 2023, 2022])

                with columns[1]:
                    selectedRegion = st.selectbox("Select Region", ["Europe", "Asia", "America", "Africa", "Oceania"])


                # Default values
                year = 2024
                region = "Europe"

                # Update values if changed
                if selectedRegion != region:
                    region = selectedRegion
                if selectedYear != year:
                    year = selectedYear

            # Get the living expenses data for the selected year and region
            dataframe = EXP.getLivingExpenses(year, region)
    
            st.caption("The table displays the living costs of different countries indexed in relation to New York (index 100)")
            st.dataframe(dataframe[["Country", "Cost of Living Index", "Rent Index", "Groceries Index", "Restaurant Price Index"]], height=500, width=1400)
            
        with exchaangespendigcalc:
            st.markdown("<p style='font-weight:bold'>Exchange Spending Calculator</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab provides a comparison of living costs for exchange students. Simply enter your spending from your home country, and it will calculate the equivalent amount needed to afford the same products and services in your chosen destination.</p>", unsafe_allow_html=True)
        # Add content for the Buying Power Overview tab here
            tabs=st.columns(2)
            lefte=tabs[0]
            righte=tabs[1]

            with lefte:
                    st.write("Enter the information of your origin country")
                    selectedRegioncalculatororigin = st.selectbox("Select Region of origin", ["Europe", "Asia", "America", "Africa", "Oceania"],key="selectregionsorigin")
                    year=2024

                    listofcountries=EXP.getLivingExpenses(year,selectedRegioncalculatororigin).iloc[1:,1].tolist()#gets a list of all the countries in selected region 
                    origin=st.selectbox("Please provide your Home-country",listofcountries)
            with righte:
                    st.write("Enter the information of your perfered destination")
                    selectedRegioncalculatordestination = st.selectbox("Select Region of prefered destination", ["Europe", "Asia", "America", "Africa", "Oceania"],key="selectregiondestination")
                    listofcountries2=EXP.getLivingExpenses(year,selectedRegioncalculatordestination).iloc[1:,1].tolist()#gets a list of all the countries in selected region 
                    destination=st.selectbox("Please provide your prefered detionation",listofcountries2)

                    button=st.button("start calculation")#to start calculation after putting in all inputs

            with lefte: 
                    with st.expander("Settings"):
                        #standard is just total amount, advanced is specified
                        checkcalculator=st.radio("Choose your prevered setting", ["standard", "advanced"] )
                        if checkcalculator=="advanced":
                            #user input of amount which gets checked if they are negativ
                            rentamountinput=int(st.number_input("Put in your rent spendings"))
                            rentamount=0
                            if rentamountinput<0:
                                st.error("Please provide initial input bigger than 0")
                            else:
                                rentamount=rentamountinput
                            #user input of amount which gets checked if they are negativ
                            grocamountinput=int(st.number_input("Put in your groc spendings"))
                            grocamount=0
                            if grocamountinput<0:
                                st.error("Please provide initial input bigger than 0")
                            else:
                                grocamount=grocamountinput
                            #user input of amount which gets checked if they are negativ
                            restaurantamountinput=int(st.number_input("Put in restaurant spendings"))
                            restaurantamount=0
                            if restaurantamountinput<0:
                                st.error("Please provide initial input bigger than 0")
                            else:
                                restaurantamount=restaurantamountinput

                            totalamount=rentamount+grocamount+restaurantamount

                            with righte:
                                if button:
                                    if totalamount==0:
                                        st.write("Please Provide Amount")
                                    else:
                                        #returns a table with the initial and exchanged amount of each category (by calling function instantly printed in streamlit)
                                        ESC.getcalculatorforexchange(selectedRegioncalculatororigin,selectedRegioncalculatordestination,origin,destination,totalamount,restaurantamount,rentamount,grocamount)
                        if checkcalculator=="standard":
                            totalamount2input=int(st.number_input("Put in your total spendings"))
                            totalamount2=0
                            #user input of amount which gets checked if they are negativ
                            if totalamount2input<0:
                                st.error("Please provide initial input bigger than 0")
                            else:
                                totalamount2=totalamount2input

                            with righte:
                                if button and totalamount2!=0:
                                    #returns a table with the initial and exchanged amount for total spending (by calling function instantly printed in streamlit)
                                    ESC.getcalculatorforexchangesimple(selectedRegioncalculatororigin,selectedRegioncalculatordestination,origin,destination,totalamount2)