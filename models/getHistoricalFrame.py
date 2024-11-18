import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests


def gettimeframe(currency1,currency2):

    key="d6f3714af7452487c54e61a84a08dff4"
    base=f"https://api.forexrateapi.com/v1/timeframe"

    startdate="2024-10-10"
    enddate="2024-10-15"

    #IMPORTANT TO UNDERSTAND
    # Alters the URL to include the API key, the start date, end date, base currency and the currency to be converted to
    request_url = f"{base}?api_key={key}&start_date={startdate}&end_date={enddate}&base={currency1}&currencies={currency2}"

    #IMPORTANT TO UNDERSTAND
    # Gets the data from the API, like when you access pinterest.com and get the images :)
    response = requests.get(request_url)


    if response.status_code == 200: #if code=200, it works well

        # Formats the data into json format: e.g. {country_code : "DK", country_name : "Denmark"}
        data = response.json()
        

        # The data["rates"] grabs the value of the key "rates" from the json data and defines it as a variable called rates (for easy access and reference...)
        rates=data["rates"]

        # Within the rates json data (similar to the dictioary structure in python), we want to grab the exchange rate for the specific currency and date
        exchangerate = {date: rates[date][currency2] for date in rates}

        
        #IMPORTANT TO UNDERSTAND
        forchart = pd.DataFrame(list(exchangerate.items()), columns=["Date", "Exchange Rate"]) # expected output: {date: [exchange rate1, exchange rate2, exchange rate3, ...]}

        
        forchart["Date"] = pd.to_datetime(forchart["Date"], errors='coerce')#fucking annoying because streamlit is dumb
        #chart=st.line_chart(forchart.set_index("Date"))

        return forchart

    else:
        # Defines the error
        error1 = st.write("Error", response.status_code)
        # Returns the error instead :)
        return error1


