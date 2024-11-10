import requests

def FetchDataFromAPI(url):

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
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
    
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        data = FetchDataFromAPI(url)
        currencies = data["rates"]
    
        #Returns a list of dictionariess with currency codes and their values e.g. USED : 1, EUR : 0.8 etc...
        return currencies