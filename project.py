import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Currency Exchange Rate Calculator") 

st.markdown("<p style='font-size:14px; text-align:center;'>Project of Pauline, Otto, Simon and Martin\n\n",unsafe_allow_html=True)

st.sidebar.header("Select a database for the currency exchange")
database=st.sidebar.selectbox("Select a database: ",("select here","manual","CSV-import","real-time"),key="database")

if database == "select here":
    print()
if database == "manual":

    st.write("The exchange rates were set manually as of 20.10.2024\n\n")
    

    st.sidebar.subheader("Which Excange rate do you like to convert? ")

    currencys=["Euro","Dollar","Pound"]
    currency1=st.sidebar.selectbox("Select the first Currency: ",(currencys),key="currency1")
    currency2=st.sidebar.selectbox("Select the Currency to convert to: ",(currencys),key="currency2")
    
    amount=st.sidebar.number_input(f"Enter Amount of {currency1} to exchange: ",value=0)

    currency1index= currencys.index(currency1)
    currency2index= currencys.index(currency2)

    #always euro,dollar,pound
    exchangerates=[[1,1.08,0.83],[0.93,1,0.77],[1.2,1.3,1]]

    rate=exchangerates[currency1index][currency2index]

    st.write(f"the exchange rate is:  {rate} ")       
             #so 1 {currency1} is {rate} {currency2}")
    #st.write(f"1 {currency1} is {rate} {currency2}")

    if amount !=0:
         st.write(f"{amount} {currency1} are {rate*amount} {currency2} ")



    #if currency1=="Euro":
    #   st.write(f"the exchange rate is:  {e[currency2index]}")
    #if currency1=="Dollar":
    #    st.write(f"the exchange rate is:  {d[currency2index]}")
    #if currency1=="Pound":
    #   st.write(f"the exchange rate is:  {p[currency2index]}")

if database == "CSV-import": 

    st.sidebar.subheader("Which Excange rate do you like to convert? ")

    currencys=["Euro","Dollar","Pound","JPY","CNY"]
    currency1=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currency1")
    #currency2=st.sidebar.selectbox("Select a Currency: ",(currencys),key="currency2")

    currency1index= currencys.index(currency1)
    #currency2index= currencys.index(currency2)

    import1= st.sidebar.file_uploader(f"Upload a CSV file containing historical {currency1} data", type=["csv"])
    #import2= st.sidebar.file_uploader(f"Upload a CSV file containing historical {currency1} data", type=["csv"])


    if import1 is not None:
            
            import1 = pd.read_csv(import1)
            
            selection=[]
            selection = import1.columns[1:].tolist()
            selectionchoosen=st.sidebar.selectbox("Select exchange: ",(selection),key="selection")

            date=[] 
            date=import1.iloc[:, 0].tolist()
            datechoosen=st.sidebar.selectbox("Select date: ",(date),key="date")
            dateindex = date.index(datechoosen)

            exchangerate=import1.loc[dateindex,selectionchoosen]

            st.write(f"the exchange rate is:  {exchangerate}")
            

            amount=st.sidebar.number_input(f"Enter Amount of {currency1} to exchange: ",value=0)

            forprint=selectionchoosen.split("-")
            if amount !=0:
                st.write(f"the exchanged amount in {forprint[1]} is: {exchangerate*amount}")


            st.write("### Historical Exchange Rates:")
            forchart=import1[[import1.columns[0], selectionchoosen]]
            st.line_chart(forchart.set_index(import1.columns[0]))