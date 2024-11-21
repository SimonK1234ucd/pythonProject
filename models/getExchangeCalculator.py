import models.getExpenseByIndex as EXP
import pandas as pd
import streamlit as st

# COMPLETED COMMENTS

def getcalculatorforexchange(SelectedRegion_1, SelectedRegion_2, origin, destination, totalamount, restaraunt, rent, groc):

    """
    Calculates and compares the cost of living between two regions based on spending categories.

    Parameters:
    - SelectedRegion_1 (str): The origin region to analyze.
    - SelectedRegion_2 (str): The destination region to analyze.
    - origin (str): City or location in the origin region.
    - destination (str): City or location in the destination region.
    - totalamount (float): Total amount spent in the origin.
    - restaraunt (float): Restaurant spending in the origin.
    - rent (float): Rent spending in the origin.
    - groc (float): Grocery spending in the origin.

    Returns:
    - tuple: A Streamlit table displaying spending comparisons and a success/error/info message.
    """

    year = 2024
    
    # Get data for the specified region
    firstRegionDataFrame = EXP.getLivingExpenses(year, SelectedRegion_1)
    secondRegionDatFrame = EXP.getLivingExpenses(year, SelectedRegion_2)
    
    # Find row indices for origin and destination
    originrow = firstRegionDataFrame[firstRegionDataFrame.iloc[:, 1] == origin]  
    destinationrow = secondRegionDatFrame[secondRegionDatFrame.iloc[:, 1] == destination]

    # to chech if there is an error
    if originrow.empty:
        # throws an error if the origin is not found
        raise ValueError(f"Origin '{origin}' not found in the data.")
    
    # to chech if there is an error
    if destinationrow.empty:
        # throws an error if the destination is not found
        raise ValueError(f"Destination '{destination}' not found in the data.")

    # Gets the first row of column 2, 3, 4 and 5 which translates to the total index, rent index, grocery index and restaurant index
    totalindex = float(originrow.iloc[0, 2])
    rentindex = float(originrow.iloc[0, 3])  
    grocindex = float(originrow.iloc[0, 4]) 
    restarauntindex = float(originrow.iloc[0, 5])  

    # Dos the same as above but for the selected destination 
    totalindex2 = float(destinationrow.iloc[0, 2])  
    rentindex2 = float(destinationrow.iloc[0, 3])  
    grocindex2 = float(destinationrow.iloc[0, 4])  
    restarauntindex2 = float(destinationrow.iloc[0, 5])  

    # Calcuates the new amount for each of the spending categories
    newtotalamount = (totalamount * (1 / totalindex)) * totalindex2
    newrentamount = (rent * (1 / rentindex)) * rentindex2
    newgrocamount = (groc * (1 / grocindex)) * grocindex2
    newrestarauntamount = (restaraunt * (1 / restarauntindex)) * restarauntindex2

    # Creates a dataframe to display the data with the spending categories and the amounts and corresponding values:
        # Total-Amount, Rent-Amount, Grocery-Amount, Restaurant Amount
        # Origin, Destination
    dataframe = pd.DataFrame({
        "Kind of spending": ["Total-Amount", "Rent-Amount", "Grocery-Amount", "Restaurant Amount"],
        origin: [totalamount, rent, groc, restaraunt],
        destination: [newtotalamount, newrentamount, newgrocamount, newrestarauntamount]
    })

    # Creates a streamlite table to display the data
    table = st.table(dataframe)
    # Compares the total amount of the origin and destination and returns a message
    if totalamount>newtotalamount:
        returntext = st.success(f"{destination} is cheaper than {origin}")
    elif totalamount<newtotalamount:
        returntext = st.error(f"{destination} is more expensive than {origin}")
    else:
        returntext = st.info(f"{destination} is as expesive as {origin}")
    
    #Returns the table and the message
    return table, returntext

def getcalculatorforexchangesimple(selectedregion, selectedregion2, origin, destination, totalamount):

    """
    Calculates and compares the overall cost of living between two regions for total spending.

    Parameters:
    - selectedregion (str): The origin region to analyze.
    - selectedregion2 (str): The destination region to analyze.
    - origin (str): City or location in the origin region.
    - destination (str): City or location in the destination region.
    - totalamount (float): Total amount spent in the origin.

    Returns:
    - tuple: A Streamlit table displaying the total spending comparison and a success/error/info message.
    """

    year = 2024
    
    # Get index data for the specified regions
    data = EXP.getLivingExpenses(year, selectedregion)
    data2 = EXP.getLivingExpenses(year, selectedregion2)
    
    # Find row indices for origin and destination
        # Gets all the rows of the second column
    originrow = data[data.iloc[:, 1] == origin]  
        # Gets all the rows of the second column
    destinationrow = data2[data2.iloc[:, 1] == destination]

    # to chech if there is an error
    if originrow.empty:
        raise ValueError(f"Origin '{origin}' not found in the data.")
    if destinationrow.empty:
        raise ValueError(f"Destination '{destination}' not found in the data.")

    # Gets the first row of column 2, which translates to the overall index for the origin and destination

    totalindex = float(originrow.iloc[0, 2])  # origin
    totalindex2 = float(destinationrow.iloc[0, 2])  # destination

    # Calculates the new total amount based on the total index of the origin and destination
    newtotalamount = (totalamount * (1 / totalindex)) * totalindex2
    
    # Initializes a dateframe, with the spending categories and the amounts and corresponding values:
    dateframe = pd.DataFrame({
        "Kind of spending": ["Total-Amount"],
        origin: [totalamount],
        destination: [newtotalamount]
    })

    # Creates a streamlite table to display the data
    table = st.table(dateframe)

    # Compares the total amount of the origin and destination and returns a message
    if totalamount>newtotalamount:
        returntext=st.success(f"{destination} is cheaper than {origin}")
    elif totalamount<newtotalamount:
        returntext=st.error(f"{destination} is more expensive than {origin}")
    else:
        returntext=st.info(f"{destination} is as expesive as {origin}")

    #Returns the table and the message
    return table, returntext