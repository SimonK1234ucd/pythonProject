import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests as re

#USED FOR LEARING APIS
#USED FOR LEARING APIS
#USED FOR LEARING APIS
#USED FOR LEARING APIS
#API 

print('''Real-Time Currency data from "x-rates.com"''')
key="857f872f321b217745bae2f6ac9bf8d7" #API key like a passwort to enter website
base="https://api.apilayer.com/exchangerates_data/latest" #acces main server

currency1="USD"#input("put in currency 1USD: ")
currency2="EUR"

#? is splitting base from request
#q is asking for inputs
request= f"{base}?base={currency1}&symbols={currency2}"
#look https://exchangeratesapi.io/documentation/ for documentation
#symboals are currencys
#rates are the actuall rate regarding to the requested currency

headers = {
    "apikey": key
}

response = re.get(request,headers=headers)

print(response.status_code)

data = response.json()

exchangerate=data["rates"][currency2]
print(exchangerate)

    