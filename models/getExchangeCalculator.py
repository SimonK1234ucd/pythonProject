import models.getExpenseByIndex as EXP
import pandas as pd
import streamlit as st


def getcalculatorforexchange(selectedregion,selectedregion2,origin,destination,totalamount,restaraunt,rent,groc):
    year=2024
    data=EXP.getLivingExpenses(year,selectedregion)

    totalindex=EXP.getLivingExpenses(year,selectedregion).loc[origin,1]
    rentindex=EXP.getLivingExpenses(year,selectedregion).loc[origin,2]
    grocindex=EXP.getLivingExpenses(year,selectedregion).loc[origin,3]
    restarauntindex=EXP.getLivingExpenses(year,selectedregion).loc[origin,4]

    totalindex2=EXP.getLivingExpenses(year,selectedregion2).loc[destination,1]
    rentindex2=EXP.getLivingExpenses(year,selectedregion2).loc[destination,2]
    grocindex2=EXP.getLivingExpenses(year,selectedregion2).loc[destination,3]
    restarauntindex2=EXP.getLivingExpenses(year,selectedregion2).loc[destination,4]

    newtotalamount=(totalamount*(1/totalindex))*totalindex2
    newrentamoaunt=(rent*(1/rentindex))*rentindex2
    newgrocamount=(groc*(1/grocindex))*grocindex2
    newrestarauntamount=(restaraunt*(1/restarauntindex))*restarauntindex2

    returndata = pd.DataFrame({
            "item": ["Total-Amount","Rent-Amount", "Grocery-Amount","Restaurant Amount"],
            "Origin": [totalamount,rent, groc,restaraunt],
            "Destination" : [newtotalamount,newrentamoaunt,newgrocamount,newrestarauntamount]
        })

    table=st.table(returndata)

    return table

