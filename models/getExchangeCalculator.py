import models.getExpenseByIndex as EXP
import pandas as pd
import streamlit as st


def getcalculatorforexchange(selectedregion, selectedregion2, origin, destination, totalamount, restaraunt, rent, groc):
    year = 2024
    
    # Get data for the specified region
    data = EXP.getLivingExpenses(year, selectedregion)
    data2 = EXP.getLivingExpenses(year, selectedregion2)
    
    # Find row indices for origin and destination
    origin_row = data[data.iloc[:, 1] == origin]  
    destination_row = data2[data2.iloc[:, 1] == destination]

    # to chech if there is an error
    if origin_row.empty:
        raise ValueError(f"Origin '{origin}' not found in the data.")
    if destination_row.empty:
        raise ValueError(f"Destination '{destination}' not found in the data.")

    # Extract values from the rows
    totalindex = float(origin_row.iloc[0, 2])  
    rentindex = float(origin_row.iloc[0, 3])  
    grocindex = float(origin_row.iloc[0, 4]) 
    restarauntindex = float(origin_row.iloc[0, 5])  

    totalindex2 = float(destination_row.iloc[0, 2])  
    rentindex2 = float(destination_row.iloc[0, 3])  
    grocindex2 = float(destination_row.iloc[0, 4])  
    restarauntindex2 = float(destination_row.iloc[0, 5])  

    # Perform calculations
    newtotalamount = (totalamount * (1 / totalindex)) * totalindex2
    newrentamount = (rent * (1 / rentindex)) * rentindex2
    newgrocamount = (groc * (1 / grocindex)) * grocindex2
    newrestarauntamount = (restaraunt * (1 / restarauntindex)) * restarauntindex2

    # Create and display a DataFrame for the results
    returndata = pd.DataFrame({
        "Kind of spending": ["Total-Amount", "Rent-Amount", "Grocery-Amount", "Restaurant Amount"],
        origin: [totalamount, rent, groc, restaraunt],
        destination: [newtotalamount, newrentamount, newgrocamount, newrestarauntamount]
    })

    table = st.table(returndata)
    if totalamount>newtotalamount:
        returntext=st.success(f"{destination} is cheaper than {origin}")
    else:
        returntext=st.error(f"{destination} is more expensive than {origin}")
    return table, returntext

