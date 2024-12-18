import pandas as pd
from pathlib import Path

# COMPLETED COMMENTS

def getFuturePP(initial, average, years):
    """
    Calculates the future purchasing power of an initial amount given an average inflation rate and number of years.

    This function uses the formula:
        Future Buying Power = initial * (1 - (average / 100)) ** years

    It validates the inputs to ensure the inflation rate and number of years are within reasonable limits.
    If the inflation rate is greater than 20% or the number of years exceeds 100, an error message is returned.

    Parameters:
        initial (float): The initial amount of money.
        average (float): The average annual inflation rate as a percentage (e.g., 5 for 5%).
        years (int): The number of years into the future.

    Returns:
        str: A formatted string describing the future buying power, or an error message if inputs are invalid.

    Raises:
        ValueError: If the inflation rate or years result in an invalid calculation.
    """
    # Validate the input values, inflation rate and years
    if average>20:
        # Stops the function from running due to return statemnet
        return ("Inflation Rate Input to Big!")

    # Check if the number of years is within a reasonable limit
    elif years>100:
        # Stops the function from running due to return statemnet
        return ("Amount of Years is to Big!")

    # if no previous conditions are met            
    else: 
        # a product of the initial amount and the inflation rate forward discounted by the number of years
        futureBuyingPower = initial * (1 - (average/100)) ** years
        # Returns the future buying power of the provided (initial) amount
        # :.f is a format specifier that formats the number to 2 decimal places
        return (f"The future buying power of {initial} is: {"{:.2f}".format(futureBuyingPower)}")
    
def getHistoricalPPlist():
    """
    Retrieves a list of all countries available in the historical inflation data file.

    This function reads the historical inflation data file (`inflation_data.csv`) and
    extracts the list of countries or regions listed in the first column of the dataset.

    Returns:
        list: A list of country names or region identifiers (strings) present in the dataset.

    Raises:
        FileNotFoundError: If the `inflation_data.csv` file is not found.
        ValueError: If the dataset is empty or improperly formatted.
    """
    file_path = Path(__file__).parent.parent / "files" / "inflation_data.csv"
    reader = pd.read_csv(file_path)

    countrylist=[]
    countrylist=reader.iloc[:, 0].tolist() #selects thhe specific colomn (the one with country list)
    return countrylist

def getHistorialPPdata(country,year,amount):
    """
    Calculates the historical purchasing power of a given amount based on inflation data.

    This function reads inflation data from the `inflation_data.csv` file and calculates
    the adjusted purchasing power of a specified amount of money for a given country and year.
    The calculation applies inflation rates iteratively from the current year back to the specified year.

    Parameters:
        country (str): The name of the country for which to retrieve inflation data.
        year (str): The target year (column header in the dataset) for the calculation.
        amount (float): The initial monetary amount to be adjusted.

    Returns:
        float: The adjusted amount based on inflation data up to the specified year.

    Raises:
        FileNotFoundError: If the `inflation_data.csv` file is not found.
        KeyError: If the specified year or country is not in the dataset.
        ValueError: If the input values are invalid or improperly formatted.
    """
    file_path = Path(__file__).parent.parent / "files" / "inflation_data.csv"
    reader = pd.read_csv(file_path)

    yearindex=reader.columns.get_loc(year)
    rowofcounty = reader.loc[reader.iloc[:, 0] == country]
    amount=amount

    for i in range(len(reader.columns)-1,yearindex,-1):
            amount = amount*(1+( (rowofcounty.iloc[0, i]/100)))
    return amount

     



