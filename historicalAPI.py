import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests



database="Real-Time"
if database=="Real-Time": 
    st.write('''Real-Time Currency data from "ForexRateAPI"''')
    st.write('''Maximum Range is 365 days, no data before 2000''')


    
    key="d6f3714af7452487c54e61a84a08dff4"
    base=f"https://api.forexrateapi.com/v1/timeframe"

    
    currencys=["EUR","USD","JPY","CNY","GBP"]
    currency1=st.sidebar.selectbox("Select the base currency to convert: ",(currencys),key="currency1")
    currency2=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currency2") 
    startdate=st.sidebar.text_input("startdate(YYYY-MM-DD): ",key="startdate") 
    enddate=st.sidebar.text_input("enddate(YYYY-MM-DD): ",key="enddate") 

  


    #IMPORTANT TO UNDERSTAND
    request_url = request_url = f"{base}?api_key={key}&start_date={startdate}&end_date={enddate}&base={currency1}&currencies={currency2}"

    #IMPORTANT TO UNDERSTAND
    response = requests.get(request_url)


    if response.status_code == 200: #if code=200, it works well

        data = response.json()
        st.write("200")
        
        rates=data["rates"]
        exchangerate = {date: rates[date][currency2] for date in rates}#dictonaryIMPORTANT TO UNDERSTAND

        #st.write("Exchange rate:", exchangerate)
        st.write("erstes:", exchangerate[startdate])
        
        forchart = pd.DataFrame(list(exchangerate.items()), columns=["Date", "Exchange Rate"])#IMPORTANT TO UNDERSTAND
        #st.write(forchart)
        forchart["Date"] = pd.to_datetime(forchart["Date"], errors='coerce')#fucking annoying because streamlit is dumb
        chart=st.line_chart(forchart.set_index("Date"))
    


    else:
        st.write("Error", response.status_code)


