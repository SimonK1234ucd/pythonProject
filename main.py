
# The main.py file is the run, that is actuall run in the brower
# Use streamlit run main.py to start the program.
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import models.getCurrencies as getCurrencies
import altair as alt
import models.getHistoricalPoint as getHistoricalPoint
import models.getHistoricalFrame as getHistoricalFrame
import models.getChartMPW as getChartMPW
import models.getreadfile as getreadfile
import models.getPurchasingPower as getPurchasingPower
from models.getreadfile import getcurrencylistE, getspecificdatedata, getcurrencychart
from models.getCurrencyRisk import display_currency_risk
from models.ExchangeSpending import display_spending_comparison

st.set_page_config(layout="wide", page_title="Exchange Tool")
# Use st.markdown to allow HTML with unsafe_allow_html=True

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

#Page Layout: 

# Sets up two columns for the page layout
columns = st.columns(2)
leftSide = columns[0]
rightSide = columns[1]


with leftSide:
    # Create tabs for Currency Converter and Historical Exchange Rates and so on
    tabs = st.tabs(["Currency Overview", "Compare Currencies", "Currencies Historically", "Purchasing Power Calculator"])

    currencyTypes = getCurrencies.getCurrencyTypes().keys() #because of keys just the KEYs is global defined




# Add content for the Currency Overview tab here
    with tabs[0]:
        st.markdown("<p style='font-weight:bold'>Overview of Currencies</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px'>The Currency Overview displays the value of a selected currency compared to other currencies.</p>", unsafe_allow_html=True)

        # Settings Expander    
        with st.expander("Settings"):
            selectedCur = st.selectbox("Select Currency", currencyTypes)
            
            # Fetch currency list for selected currency
            currencyList = getCurrencies.getSpecificCurrency(selectedCur)
            
            # Convert the currency list to a sorted list of tuples (currency, value)
            sorted_currency_data = sorted(currencyList.items(), key=lambda item: item[1])#here grabbing items, lamda for every item second value (exchange rates)
            
            # Extract values to calculate thresholds
            values = [value for currency, value in sorted_currency_data]
            median = pd.Series(values).median()
            minValue= 1
            maxValue= median +50

            threshold =(minValue, maxValue)
            sort= st.radio("Sort by Value", ("Ascending", "Descending"))

        valueColumn = f"Value of 1 {selectedCur}"

        # Convert sorted list to a DataFrame
        dataForChart = pd.DataFrame(sorted_currency_data, columns=["Currency", valueColumn])

        # Filter data based on the selected threshold
        filteredData=dataForChart[(dataForChart[valueColumn] >= threshold[0]) & (dataForChart[valueColumn] <= threshold[1])]

        # Sort data based on the selected sort order
        ascending_order = True if sort == "Ascending" else False
        filteredData = filteredData.sort_values(by=valueColumn, ascending=ascending_order)

        # Display the filtered and sorted bar chart
        chart = alt.Chart(filteredData).mark_bar().encode(
            x=alt.X("Currency", sort=None),
            y=valueColumn
        ).properties(height=400, width=550)

        st.altair_chart(chart)

        




    with tabs[1]:
        st.markdown("<p style='font-weight:bold'>Currency Converter</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px'>The Currency Converter transforms a selected currency into other specified currencies.</p>", unsafe_allow_html=True)


        #get the base currency and then create the currenylist for this currency
        curr1=st.selectbox("Select Base currency",currencyTypes)
        currencylist2=getCurrencies.getSpecificCurrency(curr1)

        #select here the currency the user like to convert to 
        curr2= st.multiselect("Select Currencies", currencyTypes, default=[ "USD","GBP", "JPY"],)

        #for loop for every of the currency 2 selected in the new currency list
        for currencies in curr2:

            st.write(f"1 {curr1} = {currencylist2[currencies]} {currencies}") #search for the exchange rate in the currency list for every of the cur 2, and print the name of the cur2 out after

    

    with tabs[2]:

        st.markdown("<p style='font-weight:bold'>Compare Euro Historically</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px'>This tab offers statistics and graphical information on the historical performance of a selected currency against the Euro.</p>", unsafe_allow_html=True)

        # Get the list of currencies
        currencylistE=getreadfile.getcurrencylistE()

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
        st.write(f"Historical Data of {curE} for the Selected Time Period ({date})")
        st.line_chart(chartplot)

        # Unused code Simon
        # Display statistics for a specific date if provided
        # st.markdown("<p style='font-weight:bold; font-size:22px'>Statistics:</p>", unsafe_allow_html=True)

        # if date: 
            # dateexrate = getreadfile.getspecificdatedata(curE, date)
            # st.write(f"Time period: {date}")
            # st.write(f"Exchange Rate: {dateexrate} {curE}")
        
        # Display currency risk assessment
        st.markdown("<p style='font-weight:bold; font-size:22px'>Currency Risk Assessment:</p>", unsafe_allow_html=True)
        display_currency_risk(curE, start_date)



        #OLD CODE
        #st.markdown("<p style='font-weight:bold'>Currency Table</p>", unsafe_allow_html=True)
        #curre1=st.selectbox("Select Base currency", currencyTypes, key="tab2")
        #currencylist3=getCurrencies.getSpecificCurrency(curre1)

        #currencydf= pd.DataFrame(list(currencylist3.items()), columns=["Currency", f"Value of 1 {curre1}"])
        #st.dataframe(currencydf, width=500, height=500)



    with tabs[3]:

        st.markdown("<p style='font-weight:bold'>Purchasing Power Calculator</p>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:14px'>This tab provides comprehensive information for a clear overview of the purchasing power of a selected currency.</p>", unsafe_allow_html=True)
       
        check=st.radio("Select checkbox:", ["Historical Purchasing Power", "Future Purchasing Power"])
        
        
        if check=="Future Purchasing Power":
            initial=st.number_input("Provide Initial Amount in EUR")
            average=st.number_input("Provide Average Inflation Rate in %  (max. 20%)")
            years=st.number_input("Provide Amount of Years  (max. 100)")

            forprint=getPurchasingPower.getFuturePP(initial,average,years)
            st.write(forprint)
        
        if check=="Historical Purchasing Power":
            with st.expander("Settings"):
                listcountrys=[]
                listcountrys=getPurchasingPower.getHistoricalPPlist()
                country=st.selectbox("Please Select the country of your interest:", listcountrys, key="tab3b")
                initial=st.number_input("Provide Amount today")
                years=st.text_input("What year do you like to know the Purchasing Power of? (YYYY)")

            if country:
                data3=getChartMPW.getchartforMPW(country)
                st.write(f"Hisorical Money Purchasing Power of {country}: ")
                st.line_chart(data3.set_index("Year"))
            
            if years and initial:
                data3b=getPurchasingPower.getHistorialPPdata(country,years,initial)
                st.write(f"The Value of {initial} in {years} is {data3b}")
            
        
        
        
        
         


        #OLD CODE
        # exchangeratedate=0
       # if check=="Click here for historical curriency converter":
        #    with st.expander("Settings"):
         #       
          #      date=st.text_input("date (YYYY-MM-DD): ",key="date") 
           #     if date:
            #        
             #       cur3=st.selectbox("Select Base currency", currencyTypes, key="tab3")
              #      cur3b=st.selectbox("Select currency to convert to", currencyTypes, key="tab3b")
               #     
                #    exchangeratedate=getHistoricalPoint.getspecificdate(date,cur3,cur3b)
                 #   #REMOVE THE# TO USE HISTORICAL FRAME !!!MANY REQUESTS!!!
                  #  chart=getHistoricalFrame.gettimeframe(cur3,cur3b)
                
          #  if date and exchangeratedate: # use that chart is not in settings but date is already selected
           #         st.write(f"On {date} :")
            #        st.write(f"1 {cur3} is {exchangeratedate} {cur3b}")
             #       st.write("Last 30-Days:")
              #      #REMOVE THE# TO USE HISTORICAL FRAME !!!MANY REQUESTS!!!
               #     chart=st.line_chart(chart.set_index("Date"))



       
    

            #with st.expander("Settings"):
             #   import1=st.file_uploader("Please upload Excel containing Historical Inflation Data")
              #  if import1 is not None:
               #     import1 = pd.read_excel(import1)
                #
                 #   #select which country
                  #  selection=[]
                   # selection = import1.iloc[:,1].tolist()
                    #selectionchoosen3=st.selectbox("Select country: ",(selection),key="country")
            
           # if import1 is not None and selectionchoosen3: # used that chart is not in settings but filed already uploaded
            ##    data3=getChartMPW.getchartforMPW(import1, selectionchoosen3)
              #  st.write(f"Hisorical Money Purchasing Power of {selectionchoosen3}: ")
               # st.line_chart(data3.set_index("Year"))

with rightSide:
    tabs = st.tabs(["Exchange Spending Calculator", "Buying Power Overview"])

    # Add content for the Living expenses tab here
    with tabs[0]:
        st.markdown("## Exchange Spending Calculator", unsafe_allow_html=True)
        display_spending_comparison()

    # Add content for the Buying Power Overview tab here
    with tabs[1]:
        st.markdown("<p style='font-weight:bold'>Buying Power Overview</p>", unsafe_allow_html=True)
        # Add content for the Buying Power Overview tab here
    
    
    # Add content for the right column


#Splitter for the page layout
st.empty()