
# Request is an external module, that allows you to make request to a server and get a response back, a.k.a an API :).
import requests
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

    print("Checking the currency types", cur)

    url = "https://api.exchangerate-api.com/v4/latest/" + cur
    data = FetchDataFromAPI(url)
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

    print("Checking the currency types")

    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    data = FetchDataFromAPI(url)
    # format of data: {'rates' : {'USD' : 1.2, 'EUR' : 1.0, 'JPY' : 0.8 etc...}, 'base' : 'EUR', 'date' : '2021-01-01'}
    currencies = data["rates"]

    #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
    return currencies