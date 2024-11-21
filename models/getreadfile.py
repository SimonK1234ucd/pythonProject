import pandas as pd
from pathlib import Path

# COMPLETED COMMENTS

def getAllCurrenciesComparedToEuro():
    """
     Retrieves a list of all currencies compared to the Euro from the historical data file.

     This function reads the historical data file (`eurohistoricaldata.csv`) and extracts
     the list of all currency codes available in the dataset, excluding the date column.

     Returns:
        list: A list of currency codes (strings) that are compared to the Euro in the dataset.

     Raises:
        FileNotFoundError: If the `eurohistoricaldata.csv` file is not found.
        IndexError: If the dataset does not contain the expected column structure.
     """

    #Retreives the file: eurohistoricaldata.csv from the files folder
    file_path= Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"

    # Initalizeses a dataframe of the retrieved file using pandas
    reader= pd.read_csv(file_path)

    # Splices the first row of the dataframe and converts it to a list (removes the date column)
    currenciesInRelationToEuro = reader.columns[1:42].tolist()

    return currenciesInRelationToEuro

def getcurrencychart(cur):
    """
    Retrieves and prepares historical exchange rate data for a specific currency.

    This function reads the historical data file (`eurohistoricaldata.csv`), extracts
    the exchange rate data for the specified currency, and formats it into a 
    DataFrame with dates as the index. The resulting DataFrame is ready for visualization
    or further analysis.

    Parameters:
        cur (str): The currency code (e.g., "USD", "GBP") for which to retrieve exchange rate data.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical exchange rate data, 
                          indexed by date with a single column for the specified currency.

    Raises:
        KeyError: If the specified currency is not found in the data.
        ValueError: If there are issues with date parsing or invalid file format.
    """


    if type (cur) != str or cur == "":
        try:
            str(cur) # Tries to convert the currency code to a string
        except ValueError:
            return "Please enter a valid currency code"
    
    cur.upper() # Converts the currency code to uppercase

    # Gets the path of the file: eurohistoricaldata.csv
    file_path = Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    
    reader = pd.read_csv(file_path) # Initializes a dataframe of the retrieved file using pandas

    # Retrieves all the rows from the specified currency column
        # Loc method, is a away to access a column/row in a dataframe by label (column e.g. name/currency/code)
    currencyData = reader.loc[:,cur]

    # Retrievs all rows from the first column of the dataframe and converts them to datetime
        # iloc, aka. the integerLocation is a way to access a column/row in a dataframe by index values
    date = reader.iloc[:,0]
    
    #Updates the date variable to a datetime object
    date = pd.to_datetime(date)

    #Creates the final dataframe with the date and currency data
    dateFrame = pd.DataFrame({
        'Date' : date, 
        cur : currencyData}
    ).set_index('Date') 

    #Returns the final dataframe that consists of the columns: Date and the specified currency
    return dateFrame

def getspecificdatedata(cur,date):
    """
    Retrieves the exchange rate for a specified currency and date from historical data.

    This function reads the historical data file (`eurohistoricaldata.csv`) and looks up
    the exchange rate for the given currency and date. It then returns the corresponding
    exchange rate.

    Parameters:
        cur (str): The currency code (e.g., "USD", "GBP") for which to retrieve the exchange rate.
        date (str): The date (in 'YYYY-MM-DD' format) for which to retrieve the exchange rate.

    Returns:
        float: The exchange rate for the specified currency and date.

    Raises:
        KeyError: If the specified date or currency is not found in the data.
    """
    # Gets the path of the file: eurohistoricaldata.csv
    file_path= Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv" 

    #Initializes a dataframe of the retrieved file using pandas
    reader= pd.read_csv(file_path)
    
    #Sets the date column as the index, aka. the first column
        # Inplace = True, means that the changes are made directly to the dataframe
    reader.set_index(reader.columns[0], inplace=True) 
     
    # Tries to retrieve the exchange rate for the specified currency and date
        # row: provided date: column: provided currency
    exchangerate = reader.loc[date, cur]

    # Returns the exchange rate for the specified currency and date
    return exchangerate
