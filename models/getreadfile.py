import pandas as pd
from pathlib import Path

def getcurrencylistE():
    file_path = Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader = pd.read_csv(file_path)

    currencylisteuro=[]
    currencylisteuro = reader.columns[1:42].tolist()

    return currencylisteuro

def getcurrencychart(cur):

    file_path = Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader = pd.read_csv(file_path)

    curdata=[]
    curdata=reader.loc[:,cur]

    date=[]
    date=reader.iloc[:,0]
    date=pd.to_datetime(date)

    forchartE=pd.DataFrame({'Date': date,cur: curdata}).set_index('Date') #IMPORTANT to Understand

    return forchartE

def getspecificdatedata(cur,date):
    file_path = Path(__file__).parent.parent / "files" / "eurohistoricaldata.csv"
    reader = pd.read_csv(file_path)
    
    reader.set_index(reader.columns[0], inplace=True) #IMPORTANT to understand
     
    exchangerate=reader.loc[date,cur]

    return exchangerate








