import requests

# COMPLETED COMMENTS

def FetchDataFromAPI(url):

    """
    This function just makes making API requests easier. It fetches data from an API and returns it in json format and handles errors if the request is unsuccessful.

    Parameters:
        url: The url of the API you want to fetch data from
    
    Returns:
        json format of whatever the API returns

    """

    # We use requests.get to get the content of the url
        # The same happens when you access e.g. youtube.com (then the content is a html page of videos :)
    response = requests.get(url)

    # Checks if the request was successful before handling it...
    if response.status_code == 200:
        # Converst to json format (so we can parse it)
        data = response.json()
        # Returns the data
        return data
    # If the request is unsuccessful, it returns an error message and the status code
    else:
        return "Error", response.status_code
    

def getSpecificCurrency(cur):

    """
    This functions gets the a specific currency and returns the currency types and their values in relation to the selected currency.

    Paramters:
        cur: (str) The currency code of the selected currency e.g. USD, EUR, JPY etc...

    Returns: 
        list: A list of dictionaries with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
    """
    # Print statement to ensure the correct currency is being checked (for admin purposes)
    print("Checking the currency types", cur)

    # Formats the URL:
    url = "https://api.exchangerate-api.com/v4/latest/" + cur
    
    # Runs the API request "handler" function to get the data
    data = FetchDataFromAPI(url)

    # Grabs the rates key from the data to get the currency values of each currency compared to the selected currency
    currencies = data["rates"]

    #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
    return currencies


def getCurrencyTypes():
    
    """
    This functions gets all the currency types and returns the currency types

    Parameters:
        None

    Returns:
        currencies: A list of dictionaries with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...

    """
    # Print statement to ensure the correct currency is being checked (for admin purposes)
    print("Checking the currency types")

    # Formats the URL, we've decied the EUR is the base currency, because we're in ireland...
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    
    # Runs the API request "handler" function to get the data
    data = FetchDataFromAPI(url)

    # format of data: {'rates' : {'USD' : 1.2, 'EUR' : 1.0, 'JPY' : 0.8 etc...}, 'base' : 'EUR', 'date' : '2021-01-01'}
    currencies = data["rates"]

    #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
    return currencies