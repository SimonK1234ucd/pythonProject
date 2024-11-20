import models.getExpenseByIndex as EXP
import pandas as pd
import streamlit as st


def getcalculatorforexchange(selectedregion, selectedregion2, origin, destination, totalamount, restaraunt, rent, groc):

    year = 2024
    
    # Get data for the specified region
    data = EXP.getLivingExpenses(year, selectedregion)
    data2 = EXP.getLivingExpenses(year, selectedregion2)
    
    # Find row indices for origin and destination
    originrow = data[data.iloc[:, 1] == origin]  
    destinationrow = data2[data2.iloc[:, 1] == destination]

    # to chech if there is an error
    if originrow.empty:
        raise ValueError(f"Origin '{origin}' not found in the data.")
    if destinationrow.empty:
        raise ValueError(f"Destination '{destination}' not found in the data.")

    # Extract values from the each of the rows
    totalindex = float(originrow.iloc[0, 2])  
    rentindex = float(originrow.iloc[0, 3])  
    grocindex = float(originrow.iloc[0, 4]) 
    restarauntindex = float(originrow.iloc[0, 5])  

    totalindex2 = float(destinationrow.iloc[0, 2])  
    rentindex2 = float(destinationrow.iloc[0, 3])  
    grocindex2 = float(destinationrow.iloc[0, 4])  
    restarauntindex2 = float(destinationrow.iloc[0, 5])  

  
    newtotalamount = (totalamount * (1 / totalindex)) * totalindex2
    newrentamount = (rent * (1 / rentindex)) * rentindex2
    newgrocamount = (groc * (1 / grocindex)) * grocindex2
    newrestarauntamount = (restaraunt * (1 / restarauntindex)) * restarauntindex2


    returndata = pd.DataFrame({
        "Kind of spending": ["Total-Amount", "Rent-Amount", "Grocery-Amount", "Restaurant Amount"],
        origin: [totalamount, rent, groc, restaraunt],
        destination: [newtotalamount, newrentamount, newgrocamount, newrestarauntamount]
    })

    table = st.table(returndata)
    if totalamount>newtotalamount:
        returntext=st.success(f"{destination} is cheaper than {origin}")
    elif totalamount<newtotalamount:
        returntext=st.error(f"{destination} is more expensive than {origin}")
    else:
        returntext=st.info(f"{destination} is as expesive as {origin}")
    return table, returntext

def getcalculatorforexchangesimple(selectedregion, selectedregion2, origin, destination, totalamount):
    year = 2024
    
    # Get data for the specified region
    data = EXP.getLivingExpenses(year, selectedregion)
    data2 = EXP.getLivingExpenses(year, selectedregion2)
    
    # Find row indices for origin and destination
    originrow = data[data.iloc[:, 1] == origin]  
    destinationrow = data2[data2.iloc[:, 1] == destination]

    # to chech if there is an error
    if originrow.empty:
        raise ValueError(f"Origin '{origin}' not found in the data.")
    if destinationrow.empty:
        raise ValueError(f"Destination '{destination}' not found in the data.")

    # Extract values from the each of the rows
    totalindex = float(originrow.iloc[0, 2])  
    
    totalindex2 = float(destinationrow.iloc[0, 2])  

    newtotalamount = (totalamount * (1 / totalindex)) * totalindex2

    returndata = pd.DataFrame({
        "Kind of spending": ["Total-Amount"],
        origin: [totalamount],
        destination: [newtotalamount]
    })

    table = st.table(returndata)
    if totalamount>newtotalamount:
        returntext=st.success(f"{destination} is cheaper than {origin}")
    elif totalamount<newtotalamount:
        returntext=st.error(f"{destination} is more expensive than {origin}")
    else:
        returntext=st.info(f"{destination} is as expesive as {origin}")
    return table, returntext