import pandas as pd

def getFuturePP(initial,average,years):
    if average>20:
        a=("Inflation Rate Input to Big!")
        return a


    elif years>100:
        b=("Amount of Years is to Big!")
        return b
            
    else: 
        FutureBuying=initial*(1-(average/100))**years
        forreturn=(f"The future buying power of {initial} is: {"{:.2f}".format(FutureBuying)}")#####NEED HELP HERE WHEN HIGH AMOUNT OUTPUT=0, IDK WHY
        return forreturn
    
def getHistoricalPPlist():
    reader=pd.read_excel("/Users/simonkoos/Desktop/github/pythonProject/files/inflation_data.xlsx")
    countrylist=[]
    countrylist=reader.iloc[:, 0].tolist()
    return countrylist

def getHistorialPPdata(country,year,amount):
     reader=pd.read_excel("/Users/simonkoos/Desktop/github/pythonProject/files/inflation_data.xlsx")
     yearindex=reader.columns.get_loc(year)
     rowofcounty = reader.loc[reader.iloc[:, 0] == country]
     amount=amount

     for i in range(len(reader.columns),yearindex):
            amount = amount*1+( (rowofcounty.iloc[0, i]/100))
     return amount

     



