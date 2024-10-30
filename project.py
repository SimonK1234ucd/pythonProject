import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Currency Exchange Rate Calculator") 

st.markdown("<p style='font-size:14px; text-align:center;'>Project of Pauline, Otto, Martin and Simon",unsafe_allow_html=True)

st.sidebar.header("Select a database for the currency exchange")
database=st.sidebar.selectbox("Select a database: ",("Select here","Manual","CSV-import","Real-time"),key="database")

if database == "Select here":
    print()
if database == "Manual":

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

    import1= st.sidebar.file_uploader(f"Upload a CSV file containing historical {currency1} data", type=["csv"], key="import1")
    #import2= st.sidebar.file_uploader(f"Upload a CSV file containing historical {currency1} data", type=["csv"])


    if import1 is not None:

            import1 = pd.read_csv(import1)
            
            #select which currency
            selection=[]
            selection = import1.columns[1:].tolist()
            selectionchoosen=st.sidebar.selectbox("Select exchange: ",(selection),key="selection")
            
            #select which date
            date=[] 
            date=import1.iloc[:, 0].tolist()
            datechoosen=st.sidebar.selectbox("Select date: ",(date),key="date")
            dateindex = date.index(datechoosen)

            #take exchange rate of selected currency/date
            exchangerate=import1.loc[dateindex,selectionchoosen]

            st.write(f"the exchange rate is:  {"{:.2f}".format(exchangerate)}")
            
            #input of amount to convert
            amount=st.sidebar.number_input(f"Enter Amount of {currency1} to exchange: ",value=0)
            
            #for print in main screen need to split because CSV always CUR1-CUR2
            forprint=selectionchoosen.split("-")
            if amount !=0:
                amountforprint=exchangerate*amount
                st.write(f"the exchanged amount in {forprint[1]} is: {"{:.2f}".format(amountforprint)}")

            #creating graph
            st.write("### Historical Exchange Rates:")
            chart = st.empty()
            forthisfirst=0 #needed for checkbox below graph

            if forthisfirst==0:
                forchart=import1[[import1.columns[0], selectionchoosen]]
                chart.line_chart(forchart.set_index(import1.columns[0]))

                checkboxaxis=st.checkbox("Would you like to compare to currencys historically? ")

            #creating overlaying axis 
            
            if checkboxaxis == True: 
                 forthisfirst=1
                 #select selection 2 of currency
                 selection2=[]
                 selection2 = import1.columns[1:].tolist()
                 selectionchoosen2=st.sidebar.selectbox("Select currency to compare: ",(selection2),key="selection2")

                #updating new chart
                 forchart=import1[[import1.columns[0], selectionchoosen, selectionchoosen2]]
                 chart.line_chart(forchart.set_index(import1.columns[0]))
            else:
                 forthisfirst=0




