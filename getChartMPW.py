import pandas as pd
import requests
import streamlit as st

def getchartforMPW(import1,selectionchoosen):
                
                #import1 = pd.read_excel(import1)
                
                #select which country
                #selection=[]
                #selection = import1.iloc[:,1].tolist()
                #selectionchoosen=st.sidebar.selectbox("Select country: ",(selection),key="country")
                
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
                        
                

                #select which date
                #date=[] 
                #date=import1.iloc[:, 0].tolist()
                #datechoosen=st.sidebar.selectbox("Select date: ",(date),key="date")
                #dateindex = date.index(datechoosen)

                #take exchange rate of selected currency/date
               # exchangerate=import1.loc[dateindex,selectionchoosen]

        
                
               #for print in main screen need to split because CSV always CUR1-CUR2
             #   forprint=selectionchoosen.split("-")
              #  if amount !=0:
               #     amountforprint=exchangerate*amount
                #    st.write(f"the exchanged amount in {forprint[1]} is: {"{:.2f}".format(amountforprint)}")''

                #creating graph
              #  st.write("### Historical Exchange Rates:")
               # chart = st.empty()
       ##
        #        forchart=import1[[import1.columns[0], selectionchoosen]]
         #           chart.line_chart(forchart.set_index(import1.columns[0]))