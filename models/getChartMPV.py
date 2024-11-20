import pandas as pd
import streamlit as st
from pathlib import Path


# This function illustrates the evolution of the money purchasing power of a country
def CountryPurchasingPower(selectedCountry):

        """
        Gets the purchasing power of a country given by a paramter



        Parameters:
        selectedCountry (str): The country selected by the user e.g. "United States"

        Returns: 
        DataFrame: A dataframe containing the years and the purchasing power of the country
        e.g.        Year       Value
                0  1970-01-01  100.000000


        """

        # Check if the selected country is a string        
        if type (selectedCountry) != str or selectedCountry == "":
                return st.error("Please select a country")

        # Gets the path of the file...
        file_path = Path(__file__).parent.parent / "files" / "inflation_data.xlsx"

        #Reads the data from the file and assigns it to the variable file
        file = pd.read_excel(file_path) # eturns a dataframe
        

        # Gets the data related the selected country
        country = file[file['Country'] == selectedCountry]

        # Check if the country exists in the data
        if country.empty:
                return st.error("Selected country not found in the data")

        # Input format: [Year, Country, Value]   Output format: [Value1, Value2, Value3]
        # country is a dataframe
        # iloc converts the dataframe to an array

        countryValues = country.iloc[:, 2:].values.flatten().tolist()

        # Calculates the money of the country in the year 1970
        moneyValue = 100
        
        dataForChart = [100]

        # Calculates the money purchasing power of the country for each year
        for year in countryValues: 
                # Money value decreases by the inflation rate
                moneyValue = moneyValue*(1- (year / 100))
                dataForChart.append(moneyValue)

        #st.line_chart(dataforchart.set_index('Year'))
        years = list(range(1970, 1970 + len(dataForChart)))

        # Create a dataframe with the data to be displayed in the chart
        dataFrame = pd.DataFrame({
                "Year": years,
                "Value": dataForChart })

        # Convert the year to datetime so it can be displayed in the chart
        dataFrame["Year"] = pd.to_datetime(dataFrame["Year"], format='%Y',errors='coerce')

        return dataFrame

