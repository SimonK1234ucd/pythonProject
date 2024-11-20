import pandas as pd
from pathlib import Path

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

    file_path= Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader= pd.read_csv(file_path)

    currencylisteuro=[]
    currencylisteuro = reader.columns[1:42].tolist()

    return currencylisteuro

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


    file_path= Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader= pd.read_csv(file_path)

    curdata=[]
    curdata=reader.loc[:,cur]

    date=[]
    date=reader.iloc[:,0]
    date=pd.to_datetime(date)

    forchartE=pd.DataFrame({'Date': date,cur: curdata}).set_index('Date') #IMPORTANT to Understand

    return forchartE

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

    file_path= Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader= pd.read_csv(file_path)
    
    reader.set_index(reader.columns[0], inplace=True) #IMPORTANT to understand
     
    exchangerate=reader.loc[date,cur]

    return exchangerate
