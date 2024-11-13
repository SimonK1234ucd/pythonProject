import requests
import streamlit as st


def getspecificdate(date,currency1,currency2):
                
                key="d6f3714af7452487c54e61a84a08dff4"
                base=f"https://api.forexrateapi.com/v1/{date}"
            
                request_url = f"{base}?api_key={key}&base={currency1}&currencies={currency2}"
                response = requests.get(request_url)

                if response.status_code == 200: #if code=200, it works well
                    
                    data = response.json()
                    #st.write("200")

                    exchangerate = data["rates"][currency2]
                    exchangerate = "{:.2f}".format(exchangerate)
                    return  exchangerate

                else:
                    return st.write("Error", response.status_code)
