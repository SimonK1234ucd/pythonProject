import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests


def gettimeframe(currency1,currency2):
    #st.write('''Real-Time Currency data from "ForexRateAPI"''')
    #st.write('''Maximum Range is 365 days, no data before 2000''')


    
    key="d6f3714af7452487c54e61a84a08dff4"
    base=f"https://api.forexrateapi.com/v1/timeframe"

    
    #currencys=["EUR","USD","JPY","CNY","GBP"]
    #currency1=st.sidebar.selectbox("Select the base currency to convert: ",(currencys),key="currency1")
    #currency2=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currency2") 
    startdate="2024-10-10"
    enddate="2024-10-15"



    #IMPORTANT TO UNDERSTAND
    request_url = request_url = f"{base}?api_key={key}&start_date={startdate}&end_date={enddate}&base={currency1}&currencies={currency2}"

    #IMPORTANT TO UNDERSTAND
    response = requests.get(request_url)


    if response.status_code == 200: #if code=200, it works well

        # Formats the data into json format: e.g. {country_code : "DK", country_name : "Denmark"}
        data = response.json()
        #st.write("200")
        
        # The data["rates"] grabs the value of the key "rates" from the json data and defines it as a variable called rates (for easy access and reference...)
        rates=data["rates"]

        # Within the rates json data (similar to the dictioary structure in python), we want to grab the exchange rate for the specific currency and date
        exchangerate = {date: rates[date][currency2] for date in rates}

        
        #IMPORTANT TO UNDERSTAND
        forchart = pd.DataFrame(list(exchangerate.items()), columns=["Date", "Exchange Rate"]) # expected output: {date: [exchange rate1, exchange rate2, exchange rate3, ...]}
            

        #st.write(forchart)
        forchart["Date"] = pd.to_datetime(forchart["Date"], errors='coerce')#fucking annoying because streamlit is dumb
        #chart=st.line_chart(forchart.set_index("Date"))

        return forchart
    


    else:
        error1=st.write("Error", response.status_code)
        return error1


