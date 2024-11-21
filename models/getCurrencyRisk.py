import streamlit as st
import pandas as pd
import numpy as np
from models.getreadfile import getcurrencychart
from datetime import date

# COMPLETE COMMENTS
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

    # A simple if statement, that returns a status report based on the volatility

    if volatility < 1: # if the volatility is less than 1, the currency is considered stable
        
        return "Low", "Low Volatility: The currency is relatively stable."    
    elif 1 <= volatility < 3: # if the volatility is between 1 and 3, the currency is considered to have moderate fluctuations
        
        return "Medium", "Medium Volatility: The currency has moderate fluctuations."
    else: # if the volatility is greater than 3, the currency is considered to have significant fluctuations
        
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
        # Fetch historical exchange rate data for the given currency
        data = getcurrencychart(cur)
        
        # Check if data exists (not None or empty)
        if data is None or data.empty:
            st.error("No data available for the selected currency.")
            return None, None

        # Convert the index of the DataFrame to datetime for easier date-based filtering
        data.index = pd.to_datetime(data.index)

        # Filter data to include only entries on or after the specified start date
        filtereddata = data[data.index >= start_date].copy()
        if filtereddata.empty:
            st.error("No data available within the specified date range.")
            return None, None

        # Convert the currency column to numeric values, replacing invalid entries with 0
        filtereddata[cur] = pd.to_numeric(filtereddata[cur], errors='coerce').fillna(0)
        # .fillna(0): Replaces any NaN values (e.g., from parsing errors) with 0

        # Calculate the absolute percentage change in currency values day-over-day
        filtereddata['Pct_Change'] = (
            filtereddata[cur]
            .pct_change()  # Calculates day-to-day percentage change
            .abs()         # Takes the absolute value of the percentage change
            .fillna(0)     # Replaces NaN values (e.g., for the first row) with 0
            * 100          # Converts to percentage format
        )

        # Calculate the most recent daily volatility (last 252 trading days)
        data['Pct_Change'] = (
            data[cur]
            .pct_change()   # Day-to-day percentage change
            .tail(252)      # Selects the last 252 rows (approx. one year of trading days)
            .fillna(0)      # Replaces any NaN values in the subset with 0
        )
        recent_daily_volatility = data['Pct_Change'].tail(252).std()  # Standard deviation of daily changes
        # .std(): Computes the standard deviation, a measure of volatility in daily returns

        # Annualize the daily volatility using the square root of trading days per year
        recent_annual_volatility = recent_daily_volatility * (252 ** 0.5)

        # Assess the risk level based on annual volatility (e.g., "Low", "Medium", "High")
        risk_level, risk_message = assess_risk_level(recent_annual_volatility)

        # Calculate the maximum drawdown (largest drop from peak to trough)
        filtereddata['Cumulative_Max'] = filtereddata[cur].cummax()  # Running maximum value over time
        filtereddata['Drawdown'] = (
            (filtereddata[cur] - filtereddata['Cumulative_Max']) / filtereddata['Cumulative_Max']
        )
        filtereddata['Drawdown'] = filtereddata['Drawdown'].fillna(0)  # Replace NaN (from division by zero) with 0
        max_drawdown = filtereddata['Drawdown'].min() * 100  # Minimum drawdown (as percentage)

        # Calculate additional metrics
        mean_return = filtereddata['Pct_Change'].tail(252).mean()  # Average daily return over the last 252 days
        annualmeanreturn = mean_return * 252  # Annualized mean return
        value_range = (
            filtereddata[cur].tail(252).max() - filtereddata[cur].tail(252).min()
        )  # Difference between max and min values in the past year
        variance = filtereddata['Pct_Change'].tail(252).var()  # Variance of daily returns
        # .var(): Measures variability in returns (spread of data)

        # Sharpe ratio: Risk-adjusted return (mean return divided by volatility)
        sharpe_ratio = mean_return / recent_daily_volatility if recent_daily_volatility != 0 else np.nan

        # Create two Streamlit columns for displaying data
        [links, rechts] = st.columns(2)

        # Display key metrics in a table in the left column
        risk_data = pd.DataFrame({
            "Metric": ["Start-Date", "Most Recent Annual Volatility", "Maximum Drawdown", 
                       "Mean % Change", "Range", "Variance", "Sharpe Ratio"],
            "Value": [
                start_date.date(),
                f"{recent_annual_volatility:.2f}%", 
                f"{max_drawdown:.2f}%", 
                f"{mean_return:.2f}%", 
                f"{value_range:.2f}", 
                f"{variance:.2f}", 
                f"{sharpe_ratio:.2f}" if not np.isnan(sharpe_ratio) else "N/A"
            ]
        })
        with links:
            st.caption("The table shows statistics of the last year:")
            st.table(risk_data)

        # Prepare data for plotting the daily percentage changes
        filtereddata.index.name = 'index'  # Ensure the index is named for use in plotting
        forchart = filtereddata[['Pct_Change']].reset_index()  # Reset index to use as a column in the chart

        with rechts:
            # Plot the daily percentage changes over time
            if 'index' in forchart.columns:
                st.caption("The chart plots the daily changes in the currency exchange rate:")
                st.line_chart(forchart.set_index('index')['Pct_Change'], height=300)
            else:
                st.error("The 'index' column is missing after reset_index().")

        # Return the most recent annual volatility and the risk level
        return recent_annual_volatility, risk_level

    except Exception as e:
        # Handle unexpected errors and display an error message
        st.error(f"An error occurred: {e}")
        return None, None