from bs4 import BeautifulSoup
import pandas as pd
import requests

def getLivingExpenses(year, region=None):
    # Values are indexed relative to New York City (NYC) as the base city

    regions = {
        "America" : "019",
        "Europe" : "150",
        "Asia" : "142",
        "Africa" : "002",
        "Oceania" : "009",
    }

    if region:
        url = f"https://www.numbeo.com/cost-of-living/rankings_by_country.jsp?title={year}&region={regions[region]}"
    else:
        url = f"https://www.numbeo.com/cost-of-living/rankings_by_country.jsp?title={year}"    

    response = requests.get(url)
    
    if response.status_code != 200:
        print("Failed to retrieve data.")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Locate table with id 't2'
    table = soup.find("table", {"id": "t2"})
    if not table:
        print("Table not found on the page.")
        return
    
    tbody = table.find("tbody")
    theader = table.find("thead")

    # Extract headers
    headers = [th.text.strip() for th in theader.find_all("th")]
    
    # Extract rows
    data = []
    for tr in tbody.find_all("tr"):
        row = [td.text.strip() for td in tr.find_all("td")]
        data.append(row)

    # Create DataFrame
    dataframe = pd.DataFrame(data, columns=headers)

    # Display the DataFrame
    print("Returning, DataFrame:", dataframe.count())
    return dataframe    

getLivingExpenses(2021, "Europe")