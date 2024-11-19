import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.getreadfile import getcurrencychart
import numpy as np
import time
from datetime import date

def assess_risk_level(volatility):
    if volatility < 1:
        return "Low", "Low Volatility: The currency is relatively stable."
    elif 1 <= volatility < 3:
        return "Medium", "Medium Volatility: The currency has moderate fluctuations."
    else:
        return "High", "High Volatility: Significant fluctuations may occur."


# Function to assess the currency risk and return the visuals
def display_currency_risk(cur):
   # try:
        # Get the current date
        start_date = pd.Timestamp(date.today())
        st.markdown(f"Assessing currency risk for {cur} as of {start_date.date()}")
        
        # Get historical data for the selected currency
        data = getcurrencychart(cur)
        data.index = pd.to_datetime(data.index)  # Ensure datetime index

        # Filter and calculate stats
        filtered_data = data[data.index >= start_date].copy()

        filtered_data['Pct_Change'] = filtered_data[cur].pct_change().abs().fillna(0) * 100
        print(filtered_data)
        data['Pct_Change'] = data[cur].pct_change().fillna(0)

        recent_daily_volatility = data['Pct_Change'].tail(252).std()
        recent_annual_volatility = recent_daily_volatility * (252 ** 0.5)

        risk_level, risk_message = assess_risk_level(recent_annual_volatility)

        # Calculate Maximum Drawdown
        filtered_data['Cumulative_Max'] = filtered_data[cur].cummax()
        filtered_data['Drawdown'] = (filtered_data[cur] - filtered_data['Cumulative_Max']) / filtered_data['Cumulative_Max']
        max_drawdown = filtered_data['Drawdown'].min() * 100

        # Display Statistics
        risk_data = pd.DataFrame({
            "Metric": ["Most Recent Annual Volatility", "Maximum Drawdown"],
            "Value": [f"{recent_annual_volatility:.2f}%", f"{max_drawdown:.2f}%"]
        })

        st.table(risk_data)
        st.info(risk_message)

        # Prepare data for plotting
        filtered_data.index.name = 'index'  # Ensure index has a name



        forchart = filtered_data[['Pct_Change']].reset_index()

        st.line_chart(forchart.set_index('index')['Pct_Change'], height=200)

    
        return recent_annual_volatility, risk_level
   # except Exception as e:
    #    st.error(f"Error in currency risk assessment: {e}")
     #   return None, None
