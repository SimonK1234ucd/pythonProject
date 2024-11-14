import pandas as pd
import requests
import streamlit as st

# The purpose of this file is to generate a chart given the parameters: import1 and selectionchoosen
        # import1: the dataframe containing the data e.g. [Year, Country, Value]
        # selectionchoosen: the country selected by the user e.g. "USA"

def getchartforMPW(selectionchoosen):
        import1 = pd.read_excel("/Users/simonkoos/Desktop/github/pythonProject/files/inflation_data.xlsx")      
        country = import1[import1['Country'] == selectionchoosen]
        valuescountry=country.iloc[:, 2:].values.flatten().tolist()
        moneyvalue=100
        dataforchart=[100]
        for year in valuescountry: 
                moneyvalue=moneyvalue*(1-(year/100))
                dataforchart.append(moneyvalue)
        
        #st.line_chart(dataforchart.set_index('Year'))
        years = list(range(1970, 1970 + len(dataforchart)))
        data3 = pd.DataFrame({"Year": years,"Value": dataforchart })
        data3["Year"] = pd.to_datetime(data3["Year"], format='%Y',errors='coerce')
        
        return data3
        