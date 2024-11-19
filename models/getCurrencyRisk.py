import streamlit as st
import pandas as pd
import numpy as np
from models.getreadfile import getcurrencychart
from datetime import date

def assess_risk_level(volatility):
    if volatility < 1:
        return "Low", "Low Volatility: The currency is relatively stable."
    elif 1 <= volatility < 3:
        return "Medium", "Medium Volatility: The currency has moderate fluctuations."
    else:
        return "High", "High Volatility: Significant fluctuations may occur."

# Function to assess the currency risk and return the visuals
def display_currency_risk(cur,start_date):
    try:
        # Get the current date
       #start_date = pd.Timestamp(date.today()) - pd.Timedelta(days=30)  # Consider past 30 days
        #st.markdown(f"Assessing currency risk for {cur} as of {start_date.date()}")

        # Get historical data for the selected currency
        data = getcurrencychart(cur)
        if data is None or data.empty:
            st.error("No data available for the selected currency.")
            return None, None

        data.index = pd.to_datetime(data.index)  # Ensure datetime index
        

        # Filter and calculate stats
        filtered_data = data[data.index >= start_date].copy()
        if filtered_data.empty:
            st.error("No data available within the specified date range.")
            return None, None

        # Ensure data is numeric
        filtered_data[cur] = pd.to_numeric(filtered_data[cur], errors='coerce').fillna(0)

        # Calculate Percentage Change
        filtered_data['Pct_Change'] = filtered_data[cur].pct_change().abs().fillna(0) * 100
        
        # Calculate recent volatility
        data['Pct_Change'] = data[cur].pct_change().fillna(0)
        recent_daily_volatility = data['Pct_Change'].tail(252).std()
        recent_annual_volatility = recent_daily_volatility * (252 ** 0.5)

        risk_level, risk_message = assess_risk_level(recent_annual_volatility)

        # Calculate Maximum Drawdown
        filtered_data['Cumulative_Max'] = filtered_data[cur].cummax().replace(0, np.nan)
        filtered_data['Drawdown'] = (filtered_data[cur] - filtered_data['Cumulative_Max']) / filtered_data['Cumulative_Max']
        filtered_data['Drawdown'] = filtered_data['Drawdown'].fillna(0)
        max_drawdown = filtered_data['Drawdown'].min() * 100

        [links,rechts]=st.columns(2)

        # Display Statistics
        risk_data = pd.DataFrame({
            "Metric": ["Start-Date","Most Recent Annual Volatility", "Maximum Drawdown"],
            "Value": [start_date.date(),f"{recent_annual_volatility:.2f}%", f"{max_drawdown:.2f}%"]
        })
        with links:
            st.table(risk_data)
        st.info(risk_message)

        # Prepare data for plotting
        filtered_data.index.name = 'index'  # Ensure index has a name
        forchart = filtered_data[['Pct_Change']].reset_index()  # Reset index to create 'index' column
        

        with rechts:
            if 'index' in forchart.columns:
                st.line_chart(forchart.set_index('index')['Pct_Change'], height=300)
            else:
                st.error("The 'index' column is missing after reset_index().")

        return recent_annual_volatility, risk_level

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None
