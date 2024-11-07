import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

#USED FOR LEARING APIS
#USED FOR LEARING APIS
#USED FOR LEARING APIS
#USED FOR LEARING APIS

print('''Real-Time Currency data from "FreeCurrencyAPI"''')

key = "fca_live_sy8WFnkv1nXdkCLP5RklEyRX8CXjOlOMY85GMNxH"  #key 150times
base = "https://api.freecurrencyapi.com/v1/latest"


currency1 = "USD"  
currency2 = "EUR"  

#IMPORTANT TO UNDERSTAND
request_url = request_url = f"{base}?apikey={key}&base_currency={currency1}&currencies={currency2}"

#IMPORTANT TO UNDERSTAND
response = requests.get(request_url,)


if response.status_code == 200: #if code=200, it works well

    data = response.json()
    exchangerate = data["data"][currency2]
    print(exchangerate)
else:
    print("Error", response.status_code)