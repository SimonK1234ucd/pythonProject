import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests


def gettimeframe(currency1,currency2):
    """
    Retrieves historical exchange rates for a specified timeframe between two currencies.

    This function fetches exchange rate data from the ForexRateAPI for a specified range of dates.
    It formats the data into a pandas DataFrame for further analysis or visualization.

    Parameters:
        currency1 (str): The base currency code (e.g., "USD", "EUR").
        currency2 (str): The target currency code (e.g., "GBP", "JPY").

    Returns:
        pandas.DataFrame: A DataFrame containing two columns:
            - "Date": The date of each exchange rate.
            - "Exchange Rate": The exchange rate between the two currencies on that date.
        If the API call fails, returns an error message with the HTTP status code.

    Raises:
        HTTPError: If the API returns a non-200 status code.
        ValueError: If the response is not in the expected format or keys are missing.

    Notes:
        - Requires a valid API key to access the ForexRateAPI.
        - Adjust `startdate` and `enddate` within the function to set a different timeframe.
        - The DataFrame's "Date" column is parsed as datetime for easier time-series analysis.

    Example:
         df = gettimeframe("USD", "EUR")
         print(df.head())
        # Output:
        #         Date  Exchange Rate
        # 2024-10-10         0.95
        # 2024-10-11         0.96
        # ...
    """

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


