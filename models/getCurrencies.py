
# Request is an external module, that allows you to make request to a server and get a response back, a.k.a an API :).
import requests
def FetchDataFromAPI(url):

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

    print("Checking the currency types", cur)

    url = "https://api.exchangerate-api.com/v4/latest/" + cur
    data = FetchDataFromAPI(url)
    currencies = data["rates"]

    #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
    return currencies


def getCurrencyTypes():
    
        print("Checking the currency types")
    
        url = "https://api.exchangerate-api.com/v4/latest/EUR"
        data = FetchDataFromAPI(url)
        currencies = data["rates"]
    
        #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
        return currencies