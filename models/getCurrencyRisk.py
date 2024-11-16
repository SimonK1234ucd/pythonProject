import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from models.getreadfile import getcurrencychart
import numpy as np

# Set the current date explicitly for testing or real usage
current_date = pd.to_datetime("2024-11-13")

# Function to assess the currency risk and return the visuals
def display_currency_risk(cur, start_date):
    
    # Get historical data for the selected currency
    data = getcurrencychart(cur)

    # Filter the data based on the selected time period
    filtered_data = data[data.index >= start_date]

    # Calculate the percentage change on the filtered data
    filtered_data['Pct_Change'] = filtered_data[cur].pct_change().abs() * 100

    # Calculate percentage change and volatility
    data['Pct_Change'] = data[cur].pct_change().fillna(0)
    
    # Calculate the most recent monthly volatility (last 12 months)
    recent_daily_volatility = data['Pct_Change'].tail(252).std()

    # Annualize the volatility
    recent_annual_volatility = recent_daily_volatility * (252 ** 0.5)

    # Determine risk level
    if recent_annual_volatility < 1:
        risk_level = "Low"
        risk_message = "Low Volatility: The currency is relatively stable."
    elif 1 <= recent_annual_volatility < 3:
        risk_level = "Medium"
        risk_message = "Medium Volatility: The currency has moderate fluctuations."
    else:
        risk_level = "High"
        risk_message = "High Volatility: Significant fluctuations may occur."
    
    # Calculate Value at Risk (VaR) at 95% confidence level
    #var_95 = np.percentile(filtered_data['Pct_Change'].dropna(), 5)

    # Calculate Maximum Drawdown
    #filtered_data['Cumulative_Max'] = filtered_data[cur].cummax()
    #filtered_data['Drawdown'] = (filtered_data[cur] - filtered_data['Cumulative_Max']) / filtered_data['Cumulative_Max']
   # max_drawdown = filtered_data['Drawdown'].min() * 100  # Convert to percentage

    # Display risk assessment in Streamlit
    st.markdown(f"Most Recent annual Volatility: {recent_annual_volatility:.2f}%")
    #st.markdown(f"Value at Risk: {var_95:.2f}%")
    #st.markdown(f"Maximum Drawdown: {max_drawdown:.2f}%")

    # Prepare DataFrame for the percentage change chart
    forchart = pd.DataFrame({
        "Date": filtered_data.index,
        "Percentage Change": filtered_data['Pct_Change']
    })

    # Convert "Date" column to datetime
    forchart["Date"] = pd.to_datetime(forchart["Date"], errors='coerce')

    # Plot the percentage change using Streamlit's built-in line chart
    st.line_chart(forchart.set_index("Date")["Percentage Change"])

    # Display risk assessment
    st.info(risk_message)

    return recent_annual_volatility, risk_level