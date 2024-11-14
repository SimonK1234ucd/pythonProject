import streamlit as st

def InitiateDatabase(database):
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
    if database == "Real-time": 
        #API 
        counter=0
        if counter==0:
            st.write('''Real-Time Currency data from "FreeCurrencyAPI"''')

            key="fca_live_iak4GkCgv76YYLnU90blnKibVl6sMtKSqMthUmzY"  #key 150times
            base="https://api.freecurrencyapi.com/v1/latest"
            #
            
            currencys=["EUR","USD","JPY","CNY","GBP"]
            currency1=st.sidebar.selectbox("Select the base currency to convert: ",(currencys),key="currency1")
            currency2=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currency2") 

            #IMPORTANT TO UNDERSTAND
            request_url = request_url = f"{base}?apikey={key}&base_currency={currency1}&currencies={currency2}"

            #IMPORTANT TO UNDERSTAND
            response = requests.get(request_url,)


            if response.status_code == 200: #if code=200, it works well

                data = response.json()
                exchangerate = data["data"][currency2]
                st.write(f"the exchange rate is :""{:.2f}".format(exchangerate))
                amount=st.sidebar.number_input(f"Enter Amount of {currency1} to exchange: ",value=0)
                if amount !=0:
                        amountforprint=exchangerate*amount
                        st.write(f"the exchanged amount in {currency2} is: {"{:.2f}".format(amountforprint)}")
            else:
                st.write("Error", response.status_code)



    if database=="Historical":
        chose1=st.sidebar.selectbox("Select a timeframe or one historical date: ",("Select here","Time-Frame","Time-Point"),key="choseidk")
        st.write('''Real-Time Currency data from "ForexRateAPI"''')
        st.write('''Maximum Range is 365 days, no data before 2000''')    

        if chose1=="Select here":
            print()

        if chose1=="Time-Frame":
                        
            key="d6f3714af7452487c54e61a84a08dff4"
            base=f"https://api.forexrateapi.com/v1/timeframe"

                        
            currencys=["EUR","USD","JPY","CNY","GBP"]
            currency1=st.sidebar.selectbox("Select the base currency to convert: ",(currencys),key="currencyone")
            currency2=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currencytwo") 
            startdate=st.sidebar.text_input("startdate(YYYY-MM-DD): ",key="startdate") 
            enddate=st.sidebar.text_input("enddate(YYYY-MM-DD): ",key="enddate") 

                    

            if enddate!="":
                #IMPORTANT TO UNDERSTAND
                request_url = f"{base}?api_key={key}&start_date={startdate}&end_date={enddate}&base={currency1}&currencies={currency2}"

                #IMPORTANT TO UNDERSTAND
                response = requests.get(request_url)


                if response.status_code == 200: #if code=200, it works well

                    data = response.json()
                    st.write("200")
                                
                    rates=data["rates"]
                    exchangerate = {date: rates[date][currency2] for date in rates}#dictonaryIMPORTANT TO UNDERSTAND

                    #st.write("Exchange rate:", exchangerate)
                    st.write("first:", exchangerate[startdate])
                                
                    forchart = pd.DataFrame(list(exchangerate.items()), columns=["Date", "Exchange Rate"])#IMPORTANT TO UNDERSTAND
                    #st.write(forchart)
                    forchart["Date"] = pd.to_datetime(forchart["Date"], errors='coerce')#fucking annoying because streamlit is dumb
                    chart=st.line_chart(forchart.set_index("Date"))
                            


                else:
                    st.write("Error", response.status_code)
                    
        
        if chose1=="Time-Point":
            
            date=st.sidebar.text_input("date (YYYY-MM-DD): ",key="date") 

            currencys=["EUR","USD","JPY","CNY","GBP"]
            currency1=st.sidebar.selectbox("Select the base currency to convert: ",(currencys),key="currencyone1")
            currency2=st.sidebar.selectbox("Select the currency to convert: ",(currencys),key="currencytwo2")
            if date:
                key="d6f3714af7452487c54e61a84a08dff4"
                base=f"https://api.forexrateapi.com/v1/{date}"
            
                request_url = f"{base}?api_key={key}&base={currency1}&currencies={currency2}"
                response = requests.get(request_url)

                if response.status_code == 200: #if code=200, it works well
                    
                    data = response.json()
                    #st.write("200")

                    exchangerate = data["rates"][currency2]
                    st.write("exchangerate:", "{:.2f}".format(exchangerate))

                else:
                    st.write("Error", response.status_code)
