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
            st.caption("This tab offers statistics and graphical information on the historical performance of a selected currency against the Euro.")

            currencylistE = getreadfile.getAllCurrenciesComparedToEuro() # Get the list of all the currencies against the euro

            [left, right] = st.columns(2) # Create two columns for side-by-side selection boxes

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

            # –––– FUTURE COLUMN ––––
            with future:
                st.write("Future Purchasing Power Calulator")
                futureExpander = st.expander("Future PPC Configuration", expanded=True)

                with futureExpander: # Declare an expander to hide the configuration options
                    
                    initialInput= float(st.number_input("Provide Initial Amount in EUR")) # User input for the initial amount in EUR, makes sure it is a float
                    if initialInput < 0: # Error check for the initial amount is less than zero aka. negative...
                        st.error("Please provide initial input bigger than 0")
                    
                    #provide and error-test inflation input
                    average = 0

                    inflationInput = int(st.number_input("Provide Average Inflation Rate in %  (max. +/- 20%)")) # User input for the average inflation rate as a percentage, but only allows values between -20 and 20

                    if inflationInput <- 20 or inflationInput > 20:
                        st.error("Please provide initial input in given range ")
                    else:
                        average = inflationInput

                    #provide and error-test year input
                    futureAvailableYears = sorted([str(year) for year in range(2024, 2124)], reverse = False) # A loop with a range of years from 2024 to 2124, which is then sorted in ascending order
                    selectedFutureYear = st.selectbox("Please Select the year of your interest:", futureAvailableYears, key="tab3d") # Selection box for the year of interest
                    yearsDiff = int(selectedFutureYear) - 2024 # Calculates the difference between the selected year and 2024

                if yearsDiff and initialInput and average != 0:
                    calculationStatement= getPurchasingPower.getFuturePP(initialInput, average, yearsDiff)#gets the future Purchasing Power ready to print
                    st.info(calculationStatement) # Prints the calculation statement as an info message


            # ––––– HISTORICAL COLUMN –––––
            with historical:
                st.write("Historical Purchasing Power Calulator") # Small title for the historical Purchasing Power Calculator
                historicalExpander = st.expander("Historical PPC Configuration", expanded=True) # Expander to hide the configuration options
                
                with historicalExpander: # Declare an expander to hide the configuration options

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
            
                    data3b = getPurchasingPower.getHistorialPPdata(country, years, initialinput) #to get historical data     

                    if initialinput != 0:
                        st.info(f"The Purchasing Power of {"{:.2f}".format(initialinput)} today is equal to {"{:.2f}".format(data3b)} in {years}")      
                    
        with purchasingPowerTab: # With the Purchasing Power tab in order to place graph in the bottom of the page outside of the columns.
                data3 = getChartMPV.CountryPurchasingPower(country) # Retrieves a dataframe from the CountryPurchasingPower function from the getChartMPV module
                st.write(f"Hisorical Money Value of {country}: (Index scaled: 100 = 1970)") # Title for the historical money value chart
                st.line_chart(data3.set_index("Year"))#data3.set_index("Year") converts Year column in index – ensures using Year as x-axis
            
            
                
    with CostofLiving: # The other main tab of the page: Cost of Living, defined in the beginning of the code
            # Changs this to a more correct labelling :)
        tabs = st.tabs(["Cost of Living Overview","Exchange Spending Calculator"])
        CoLOverview = tabs[0]
        exchaangespendigcalc = tabs[1]
        

        with CoLOverview: # Cost of Living Overview tab
            st.markdown("<p style='font-weight:bold'>Overview Cost of Living </p>", unsafe_allow_html=True) 
            st.markdown("<p style='font-size:14px'>This tab offers an overview of the cost of living across different countries around the world.</p>", unsafe_allow_html=True)

            selectWrapper = st.container() # Intializes a container for the selection boxes
            
            with selectWrapper: # Adds the selection boxes to the selectWrapper container

                [left, right] = st.columns(2) # Defines two columns for the selection boxes

                with left: # Left column for the selection boxes
                    selectedYear = st.selectbox("Select year", [2024, 2023, 2022]) # Available years for selection

                with right: # Right column for the selection boxes
                    selectedRegion = st.selectbox("Select Region", ["Europe", "Asia", "America", "Africa", "Oceania"]) # Available regions for selection


                # Default values
                year = 2024
                region = "Europe"

                # Update values if changed
                if selectedRegion != region:
                    region = selectedRegion
                if selectedYear != year:
                    year = selectedYear

            # Get the living expenses data for the selected year and region
            dataframe = EXP.getLivingExpenses(year, region) # Fetches a dateframe with the living expenses for the selected year and region from the getExpenseByIndex module
    
            st.caption("The table displays the living costs of different countries indexed in relation to New York (index 100)") # Short caption to explain the table
            st.dataframe(dataframe[["Country", "Cost of Living Index", "Rent Index", "Groceries Index", "Restaurant Price Index"]], height=500, width=1400) # Displays the dataframe in a table
            
        with exchaangespendigcalc:
            st.markdown("<p style='font-weight:bold'>Exchange Spending Calculator</p>", unsafe_allow_html=True)
            st.caption("This tab provides a comparison of living costs for exchange students. Simply enter your spending from your home country, and it will calculate the equivalent amount needed to afford the same products and services in your chosen destination.")
        
            # Add content for the Buying Power Overview tab here
            [left, right] = st.columns(2)
            
            with left:
                    st.write("Enter the information of your origin country")
                    selectedRegioncalculatororigin = st.selectbox("Select Region of origin", ["Europe", "Asia", "America", "Africa", "Oceania"],key="selectregionsorigin")
                    year=2024

                    listofcountries=EXP.getLivingExpenses(year,selectedRegioncalculatororigin).iloc[1:,1].tolist()#gets a list of all the countries in selected region 
                    origin=st.selectbox("Please provide your Home-country",listofcountries)
            with right:
                    st.write("Enter the information of your perfered destination")

                    selectedRegioncalculatordestination = st.selectbox("Select Region of prefered destination", ["Europe", "Asia", "America", "Africa", "Oceania"], key="selectregiondestination")
                    availabeCountries = EXP.getLivingExpenses(year,selectedRegioncalculatordestination).iloc[1:,1].tolist()#gets a list of all the countries in selected region 
                    
                    destination = st.selectbox("Please provide your prefered detionation", availabeCountries)

                    button = st.button("Run Expenses")#to start calculation after putting in all inputs

            with left: 
                    #standard is just total amount, advanced is specified
                    checkcalculator = st.radio("Details Level", ["Standard", "Advanced"] ).lower()
            
            with right: 
                    if checkcalculator == "advanced": # Given the user selects the advanced option
        
                        rentInput = int(st.number_input("Put in your rent spendings")) #user input of amount which gets checked if they are negativ
                        
                        groceryInput = int(st.number_input("Put in your groc spendings")) #user input of amount which gets checked if they are negativ
                        
                        restaurantInput = int(st.number_input("Put in restaurant spendings")) #user input of amount which gets checked if they are negativ
                        
                        # Checks if the any of the users input is negative
                        if rentInput < 0 or restaurantInput < 0 or groceryInput < 0:
                            st.error("Please provide an amount greater than 0 for all categories") # Error message if any of the inputs are less than zero

                        # Calculates the total amount for the advanced option    
                        advanced_totalExpenditure = rentInput + groceryInput + restaurantInput # Total spenditure

                    # If the user selects the standard option
                    elif checkcalculator == "standard":
                        standard_totalExpenditure = float(st.number_input("Put in your total spendings")) # Number input converted to float for the total spenditure
                        
                        if standard_totalExpenditure < 0: # Controls if the user input is negative
                            st.error("Please provide initial input bigger than 0") 
                        
            if button and checkcalculator=="advanced" and advanced_totalExpenditure != 0:
                #returns a table with the initial and exchanged amount of each category (by calling function instantly printed in streamlit)
                ESC.getcalculatorforexchange(selectedRegioncalculatororigin,
                                             selectedRegioncalculatordestination,
                                             origin,
                                             destination,
                                             advanced_totalExpenditure,
                                             restaurantInput,
                                             rentInput,
                                             groceryInput)

            if button and checkcalculator=="standard" and standard_totalExpenditure != 0:
                #returns a table with the initial and exchanged amount for total spending (by calling function instantly printed in streamlit)
                ESC.getcalculatorforexchangesimple(selectedRegioncalculatororigin, 
                                                   selectedRegioncalculatordestination, 
                                                   origin, 
                                                   destination, 
                                                   standard_totalExpenditure)