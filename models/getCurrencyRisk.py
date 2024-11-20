import streamlit as st
import pandas as pd
import numpy as np
from models.getreadfile import getcurrencychart
from datetime import date

def assess_risk_level(volatility):
    """
    Assesses the risk level of a currency based on its volatility.

    Parameters:
    ----------
    volatility : float
        The annualized volatility of the currency (percentage).

    Returns:
    -------
    tuple
        A tuple containing:
        - str: The risk level ("Low", "Medium", or "High").
    """

    if volatility < 1:
        return "Low", "Low Volatility: The currency is relatively stable."
    elif 1 <= volatility < 3:
        return "Medium", "Medium Volatility: The currency has moderate fluctuations."
    else:
        return "High", "High Volatility: Significant fluctuations may occur."

# Function to assess the currency risk and return the visuals
def display_currency_risk(cur, start_date):

    """
    Gets the currency risk for a given currency based on historical data and displays key metrics.

    Parameters:
    ----------
    cur : str
        The currency code (e.g., "USD", "EUR") to analyze.
    start_date : datetime.date
        The start date for filtering the historical data.

    Returns:
    -------
    tuple
        A tuple containing:
        - float: The most recent annual volatility of the currency (percentage).
        - str: The risk level ("Low", "Medium", or "High").

    """

    try:
        # Get historical data for the selected currency
        data = getcurrencychart(cur)
        if data is None or data.empty:
            st.error("No data available for the selected currency.")
            return None, None

        data.index = pd.to_datetime(data.index)  # Ensure datetime index

        # Filter and calculate stats
        filtereddata = data[data.index >= start_date].copy()
        if filtereddata.empty:
            st.error("No data available within the specified date range.")
            return None, None

        # Ensure data is numeric
        filtereddata[cur] = pd.to_numeric(filtereddata[cur], errors='coerce').fillna(0)

        # Calculate Percentage Change
        filtereddata['Pct_Change'] = filtereddata[cur].pct_change().abs().fillna(0) * 100
        
        # Calculate recent volatility
        data['Pct_Change'] = data[cur].pct_change().fillna(0)
        recent_daily_volatility = data['Pct_Change'].tail(252).std()
        recent_annual_volatility = recent_daily_volatility * (252 ** 0.5)

        risk_level, risk_message = assess_risk_level(recent_annual_volatility)

        # Calculate Maximum Drawdown
        filtereddata['Cumulative_Max'] = filtereddata[cur].cummax().replace(0, np.nan)
        filtereddata['Drawdown'] = (filtereddata[cur] - filtereddata['Cumulative_Max']) / filtereddata['Cumulative_Max']
        filtereddata['Drawdown'] = filtereddata['Drawdown'].fillna(0)
        max_drawdown = filtereddata['Drawdown'].min() * 100

        # Calculate rest
        mean_return = filtereddata['Pct_Change'].mean()
        value_range = filtereddata[cur].max() - filtereddata[cur].min()
        variance = filtereddata['Pct_Change'].var()

        sharpe_ratio = mean_return / recent_daily_volatility if recent_daily_volatility != 0 else np.nan

        [links, rechts] = st.columns(2)

        # Display 
        risk_data = pd.DataFrame({
            "Metric": ["Start-Date", "Most Recent Annual Volatility", "Maximum Drawdown", "Mean % Change", "Range", "Variance", "Sharpe Ratio"],
            "Value": [start_date.date(),f"{recent_annual_volatility:.2f}%",f"{max_drawdown:.2f}%",f"{mean_return:.2f}%",f"{value_range:.2f}",f"{variance:.2f}",f"{sharpe_ratio:.2f}" if not np.isnan(sharpe_ratio) else "N/A" ]})
        with links:
            st.table(risk_data)
        st.info(risk_message)

        # Prepare data for plotting
        filtereddata.index.name = 'index'  # Ensure index has a name
        forchart = filtereddata[['Pct_Change']].reset_index()  # Reset index to create 'index' column

        with rechts:
            if 'index' in forchart.columns:
                st.line_chart(forchart.set_index('index')['Pct_Change'], height=300)
            else:
                st.error("The 'index' column is missing after reset_index().")

        return recent_annual_volatility, risk_level

    #because data was bugged in the beginning
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None
