import pandas as pd

def getcurrencylistE():
    reader=pd.read_csv("eurohistoricaldata.csv")

    currencylisteuro=[]
    currencylisteuro = reader.columns[1:42].tolist()

    return currencylisteuro

def getcurrencychart(cur):

    reader=pd.read_csv("eurohistoricaldata.csv")

    curdata=[]
    curdata=reader.loc[:,cur]

    date=[]
    date=reader.iloc[:,0]
    date=pd.to_datetime(date)

    forchartE=pd.DataFrame({'Date': date,cur: curdata}).set_index('Date') #IMPORTANT to Understand

    return forchartE

def getspecificdatedata(cur,date):
     reader=pd.read_csv("eurohistoricaldata.csv")
     reader.set_index(reader.columns[0], inplace=True) #IMPORTANT to understand
     
     exchangerate=reader.loc[date,cur]

     return exchangerate








