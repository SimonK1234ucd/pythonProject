from bs4 import BeautifulSoup
import pandas as pd
import requests

#COMPLETED ALL COMMENTS

def getLivingExpenses(year, region=None):
    """
    Scrapes and retrieves the cost of living rankings by country for a specified year and region.

    This function fetches cost of living data from the Numbeo website and parses it into a pandas
    DataFrame. If a region is specified, the function filters the data for that region; otherwise,
    it retrieves global rankings for the specified year.

    Parameters:
        year (int): The year for which to retrieve the cost of living data (e.g., 2024).
        region (str, optional): The region to filter the data. Must be one of the following:
            - "America"
            - "Europe"
            - "Asia"
            - "Africa"
            - "Oceania"
            If not provided, global rankings are returned.

    Returns:
        pandas.DataFrame: A DataFrame containing the cost of living data with columns such as:
            - "Rank"
            - "Country"
            - "Cost of Living Index"
            - "Rent Index"
            - "Cost of Living Plus Rent Index"
            - "Groceries Index"
            - "Restaurant Price Index"
            - "Local Purchasing Power Index"
        If the data retrieval or parsing fails, the function prints an error message and returns None.

    Raises:
        requests.exceptions.RequestException: If the HTTP request fails.
        ValueError: If an invalid region is provided.
    
    """
    # Values are indexed relative to New York City (NYC) as the base city

    # Grabbed the region codes from the website to use in the URL
    availableRegions = {
        "America" : "019",
        "Europe" : "150",
        "Asia" : "142",
        "Africa" : "002",
        "Oceania" : "009",
    }

    # checks if region is provided when calling the function
    if region:
        # If region is provided, the URL is set to the region code
        url = f"https://www.numbeo.com/cost-of-living/rankings_by_country.jsp?title={year}&region={availableRegions[region]}"
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

    # The response.text is the HTML content of the page and "html.parser" is the parser used to parse the content (means to read the content)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate table with id 't2' because that is the table, that contains the data we want and is consistent on the page
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

    # This loop is set up a bit differently unlike the usualy format:
    # the aciton is declared in the first part of the loop and returns the value
    headers = [cell.text.strip() for cell in headerCellAsList]

    #Delcares an empty list to hold data records... :)
    data = []
    # Iterates through the fetched
        # tr = table row
    #Finds all rows in table body
    rows = tbody.find_all("tr")

    #Iterates through the rows
    for tr in rows:
        # Same as above, but for the rows of the table
        row = [td.text.strip() for td in tr.find_all("td")]

        #Appends the list of cells (the row basically) to the data list (so we have a list of lists)
        data.append(row)

    # Create DataFrame with panda
    dataframe = pd.DataFrame(data, columns=headers)

    # Printss a summerized version of the dataframe
    #print("Returning, DataFrame:", dataframe.count())

    # Returns the actual dataframe in standard format
    return dataframe