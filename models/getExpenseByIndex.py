from bs4 import BeautifulSoup
import pandas as pd
import requests

def getLivingExpenses(year, region=None):
    # Values are indexed relative to New York City (NYC) as the base city

    # Grabed the region codes from the website to use in the URL
    regions = {
        "America" : "019",
        "Europe" : "150",
        "Asia" : "142",
        "Africa" : "002",
        "Oceania" : "009",
    }

    # checks if region is provided when calling the function
    if region:
        # If region is provided, the URL is set to the region code
        url = f"https://www.numbeo.com/cost-of-living/rankings_by_country.jsp?title={year}&region={regions[region]}"
    else:
        # If region is not provided, the URL is set to the year
        url = f"https://www.numbeo.com/cost-of-living/rankings_by_country.jsp?title={year}"    

    # makes GET request to the URL
    response = requests.get(url)
    
    # Checks if the request was succcsfull
    if response.status_code != 200:
        print("Failed to retrieve data.")
        return
    
    # Parses the response text with BeautifulSoup
     # BeautifulSoup is a library that makes it easy to scrape information from web pages
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate table with id 't2'
    table = soup.find("table", {"id": "t2"})
    
    # if the table does not exist, return with print statement
    if not table:
        print("Table not found on the page.")
        return
    
    # The rows of the table are in the tbody tag
    tbody = table.find("tbody")
    # The headers of the table are in the thead tag
    theader = table.find("thead")

    # Extract headers
    # Strips each th (cell) of any whitespace and adds it to the list
    headerCellAsList = theader.find_all("th")
    # This loop is set up a bit differently like the usualy format:
        # the aciton is declared in the first part of the loop and returns the value in the second part of whichever datatype it is wrapped in
    headers = [cell.text.strip() for cell in headerCellAsList]
    
    # Extract rows

    #Delcares an empty list to hold data records... :)
    data = []
    # Iterates through the fetched
    for tr in tbody.find_all("tr"):
        # Same as above, but for the rows of the table
        row = [td.text.strip() for td in tr.find_all("td")]

        #Appends the list of cells (the row basically) to the data list (so we have a list of lists)
        data.append(row)

    # Create DataFrame with panda
    dataframe = pd.DataFrame(data, columns=headers)

    # Printss a summerized version of the dataframe
    print("Returning, DataFrame:", dataframe.count())

    # Retunrs the actual dataframe in standard format
    return dataframe    

getLivingExpenses(2021, "Europe")