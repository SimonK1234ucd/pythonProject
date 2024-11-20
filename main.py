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
        st.caption("This tool enables you to convert currencies, access detailed statistics, explore cost of living information, and much more.")

    with right:
        st.image("https://i.ibb.co/vjMnKrv/forupload.png[/img][/url]", width=350)

bodyContainer = st.container()

with bodyContainer:
    [currencyInformation, CostofLiving] = st.tabs(["Currency Information","Cost of Living" ])


    with currencyInformation:
        # Create tabs for Currency Converter and Historical Exchange Rates and so on
        tabs = st.tabs(["Currency Overview", "Compare Currencies", "Currencies Historically", "Purchasing Power Calculator"])
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
            values = [value for currency, value in sorted_currency_data]
            median = pd.Series(values).median()
            minValue= 1
            maxValue= median +50

            threshold =(minValue, maxValue)
                
            # Create a bar chart for the selected currency
            valueColumn = f"Exchange Rate"

            # Convert sorted list to a DataFrame
            dataForChart = pd.DataFrame(sorted_currency_data, columns=["Currency", valueColumn])

            # Filter data based on the selected threshold
            filteredData=dataForChart[(dataForChart[valueColumn] >= threshold[0]) & (dataForChart[valueColumn] <= threshold[1])]
            st.write(f"This chart displays the exchange rate of the {selectedCur} against the listed currencies:")
            sorted_data = filteredData.sort_values(by=valueColumn)
            st.bar_chart(data=sorted_data,x="Currency",y=valueColumn,height=500)
            
                     

        with compareCurrenciesTab:
            st.markdown("<p style='font-weight:bold'>Currency Converter</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>The Currency Converter transforms a selected currency into other specified currencies.</p>", unsafe_allow_html=True)

            [left, right] = st.columns(2)        
            #get the base currency and then create the currenylist for this currency
            
            with left:
                baseCurrency = st.selectbox("Select Base currency",currencyTypes) # e.g. EUR

            with right:
                amount = st.number_input("Enter Amount", value=1, step=1, format="%d") #amount of base currency
            #select here the currency the user like to convert to 


            allCurrencies =getCurrencies.getSpecificCurrency(baseCurrency)
            selectedCurrencies= st.multiselect("Select Currencies", currencyTypes, default=[ "USD","GBP", "JPY"],)
            st.caption("The exchange rates are displayed in current time and are subject to change.")


            rows = []
            headers = ["Base Currency", "Currency", "Exchange Rate", "Amount Exchanged"]

            
            for currency in selectedCurrencies:
                selectedAmountExchangeRated = amount * allCurrencies[currency]
                selectedAmountBaseCurrency = f"{amount} {baseCurrency}"
                exchangeRateForSingleBaseCurrency = allCurrencies[currency]

                rows.append([selectedAmountBaseCurrency, currency, exchangeRateForSingleBaseCurrency, selectedAmountExchangeRated])

            # Create a DataFrame from the rows
            df = pd.DataFrame(rows, columns=headers)
            st.dataframe(df, width=1250)


            st.write(f"The bar chart displays the exchange rate of the {baseCurrency} against the selected currencies.")
            st.bar_chart(df.set_index("Currency")["Exchange Rate"], height=250)
                 
        with currenciesHistoricallyTab:

            st.markdown("<p style='font-weight:bold'>Compare Euro Historically</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab offers statistics and graphical information on the historical performance of a selected currency against the Euro.</p>", unsafe_allow_html=True)

            # Get the list of currencies
            currencylistE=getreadfile.getAllCurrenciesComparedToEuro()

            # Create two columns for side-by-side selection boxes
            col1, col2 = st.columns(2)

            # Box for selecting currency
            with col1:
                curE = st.selectbox("Select Currency to Compare", currencylistE, key = "tab2a")

            # Dropdown for selecting time period (in the second column)
            time_periods = ["YTD", "1 year", "2 years", "3 years", "5 years", "10 years", "20 years"]
            with col2:
                date = st.selectbox("Select Time Period", time_periods, key = "time_period") 
            
            # Set the current date explicitly for testing or real usage
            current_date = pd.to_datetime("2024-11-13")

            # Determine the start date based on the selected time period
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

            
            # Get the historical chart data for the selected currency
            chartplot = getcurrencychart(curE)

            # Filter the data based on the selected time period
            chartplot = chartplot[chartplot.index >= start_date]

            # Display the historical chart
            st.write(f"Historical Data of the Exchange Rate of the {curE} against the EUR for the Selected Time Period ({date})")
            st.line_chart(chartplot, height=250)
            
            # Display currency risk assessment
            st.markdown("<p style='font-weight:bold; font-size:22px'>Currency Risk Assessment:</p>", unsafe_allow_html=True)
            display_currency_risk(curE,start_date)

        with purchasingPowerTab:

            st.markdown("<p style='font-weight:bold'>Purchasing Power Calculator</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:14px'>This tab provides comprehensive information for a clear overview of the purchasing power of a selected currency.</p>", unsafe_allow_html=True)
        
            #check=st.radio("Select checkbox:", ["Historical Purchasing Power", "Future Purchasing Power"])
            [historical,future]=st.columns(2)
            with future:
                st.write("Future Purchasing Power Calulator")
            #if check=="Future Purchasing Power":
                with st.expander("Settings"):
                    initial=st.number_input("Provide Initial Amount in EUR")
                    average=st.number_input("Provide Average Inflation Rate in %  (max. 20%)")
                    years=st.number_input("Provide Amount of Years  (max. 100)")
                if years and initial and average!=0:
                    forprint=getPurchasingPower.getFuturePP(initial,average,years)
                    st.info(forprint)
            
            with historical:
                st.write("Historical Purchasing Power Calulator")
                with st.expander("Settings"):
                    listcountrys=[]
                    listcountrys=getPurchasingPower.getHistoricalPPlist()
                    country=st.selectbox("Please Select the country of your interest:", listcountrys, key="tab3b")
                    initial=st.number_input("Provide Amount today")
                    years=st.text_input("What year do you like to know the Purchasing Power of? (YYYY) (Range: 1970-2023)")
                    
                    #year format check
                    checkb=False
                    if years:
                        try:
                            checka=int(years)
                        
                            if checka >=1970 and checka<=2024:
                                checkb=True

                            else: 
                                st.error("Please provide a year in given format and range")
                        except ValueError:
                            st.error("Please enter a valid year in the format YYYY.")


            if country:
                data3=getChartMPV.CountryPurchasingPower(country)#to get chart
                st.write(f"Hisorical Money Value of {country}: (Index scaled: 100 = 1970)")
               
                st.line_chart(data3.set_index("Year"))
            with historical:        
                if checkb==True and initial:
                    data3b=getPurchasingPower.getHistorialPPdata(country,years,initial)#to get historical data 
                    st.info(f"The Purchasing Power of {"{:.2f}".format(initial)} today is equal to {"{:.2f}".format(data3b)} in {years}")            
            

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
                
                year = 2024
                region = "Europe"

                if selectedRegion != region:
                    region = selectedRegion

                if selectedYear != year:
                    year = selectedYear

            dataframe = EXP.getLivingExpenses(year, region)
        


            chart_type = "line"
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

                    listofcountries=EXP.getLivingExpenses(year,selectedRegioncalculatororigin).iloc[1:,1].tolist()
                    origin=st.selectbox("Please provide your Home-country",listofcountries)
            with righte:
                    st.write("Enter the information of your perfered destination")
                    selectedRegioncalculatordestination = st.selectbox("Select Region of prefered destination", ["Europe", "Asia", "America", "Africa", "Oceania"],key="selectregiondestination")
                    listofcountries2=EXP.getLivingExpenses(year,selectedRegioncalculatordestination).iloc[1:,1].tolist()
                    destination=st.selectbox("Please provide your prefered detionation",listofcountries2)
                    button=st.button("start calculation")

            with lefte: 
                    with st.expander("Settings"):
                        checkcalculator=st.radio("Choose your prevered setting", ["standard", "advanced"] )
                        if checkcalculator=="advanced":
                   # totalamount=int(st.number_input("Put in your total spendings"))
                            rentamount=int(st.number_input("Put in your rent spendings"))
                            grocamount=int(st.number_input("Put in your groc spendings"))
                            restaurantamount=int(st.number_input("Put in restaurant spendings"))
                            totalamount=rentamount+grocamount+restaurantamount
                            with righte:
                                if button:
                                    if totalamount==0:
                                        st.write("Please Provide Amount")
                                    else:
                                        ESC.getcalculatorforexchange(selectedRegioncalculatororigin,selectedRegioncalculatordestination,origin,destination,totalamount,restaurantamount,rentamount,grocamount)
                        if checkcalculator=="standard":
                            totalamount2=int(st.number_input("Put in your total spendings"))
                            with righte:
                                if button:
                                    if totalamount2==0:
                                        st.write("Please Provide Amount")
                                    else:
                                        ESC.getcalculatorforexchangesimple(selectedRegioncalculatororigin,selectedRegioncalculatordestination,origin,destination,totalamount2)