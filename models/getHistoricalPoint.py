import requests
import streamlit as st


def getspecificdate(date,currency1,currency2):
    """
    Retrieves the exchange rate for two specified currencies on a given date from the ForexRateAPI.

    This function sends a GET request to the ForexRateAPI to fetch the historical exchange rate
    between two currencies (`currency1` as the base currency and `currency2` as the target) for a specified date.

    Parameters:
        date (str): The date for which to retrieve the exchange rate in 'YYYY-MM-DD' format.
        currency1 (str): The base currency code (e.g., "USD", "EUR").
        currency2 (str): The target currency code (e.g., "GBP", "JPY").

    Returns:
        str: The exchange rate formatted to two decimal places if the API call is successful.
        str: An error message with the HTTP status code if the API call fails.

    Raises:
        HTTPError: If the API returns a non-200 status code.
        ValueError: If the response is not in the expected format or keys are missing.

    Notes:
        - Requires an API key to access the ForexRateAPI.
        - Ensure the API key and URL are valid and active.
    """
                
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
