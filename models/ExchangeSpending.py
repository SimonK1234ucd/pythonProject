import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load city price level data from the CSV file
@st.cache_data
def load_price_levels():
    try:
        file_path = Path(__file__).parent.parent / "files" / "europe_city_price_levels_with_rent.csv"
        data = pd.read_csv(file_path)
        data["City"] = data["City"].str.strip()  # Remove any extra whitespace
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Function to display the city spending comparison
def display_spending_comparison():

    # Load the city price levels
    price_levels = load_price_levels()
    if price_levels.empty:
        st.error("Failed to load city price level data.")
        return
    
    with st.expander("Settings"):

        # Step 1: User selects their home city
        cities = price_levels["City"].tolist()
        home_city = st.selectbox("Select your home city:", cities)

        # Step 2: User inputs their typical monthly spending (excluding rent)
        monthly_spending = st.number_input("Enter your typical monthly spending (excluding rent) in EUR:", min_value=0.0, step=0.01)

        # Step 3: User inputs the length of the exchange (in months)
        exchange_length = st.number_input("Enter the length of your exchange (in months):", min_value=1, step=1)

        # Step 4: User selects a comparison city
        comparison_city = st.selectbox("Select a comparison city:", [city for city in cities if city != home_city])

    # Step 5: Calculate the estimated total spending including rent
    if st.button("Calculate Total Spending Comparison"):
        try:
            # Get the price level indices and average rent for both cities
            home_data = price_levels.loc[price_levels["City"] == home_city]
            comparison_data = price_levels.loc[price_levels["City"] == comparison_city]

            home_index = home_data["Price_Level_Index"].values[0]
            comparison_index = comparison_data["Price_Level_Index"].values[0]

            home_rent = home_data["Average_Student_Rent"].values[0]
            comparison_rent = comparison_data["Average_Student_Rent"].values[0]

            # Calculate the adjusted monthly spending (excluding rent)
            adjusted_monthly_spending = monthly_spending * (comparison_index / home_index)

            # Calculate the total monthly cost including rent
            total_monthly_cost_home = monthly_spending + home_rent
            total_monthly_cost_comparison = adjusted_monthly_spending + comparison_rent

            # Calculate the total spending for the entire exchange period
            total_spending_home = total_monthly_cost_home * exchange_length
            total_spending_comparison = total_monthly_cost_comparison * exchange_length

            # Display the results
            st.markdown(f"Monthly Spending (including rent) in {home_city}: {total_monthly_cost_home:.2f} EUR")
            st.markdown(f"Adjusted Monthly Spending (including rent) in {comparison_city}: {total_monthly_cost_comparison:.2f} EUR")
            st.markdown(f"Total Spending for {exchange_length} months in {home_city}: {total_spending_home:.2f} EUR")
            st.markdown(f"Estimated Total Spending for {exchange_length} months in {comparison_city}: {total_spending_comparison:.2f} EUR")

            # Highlight savings or extra costs
            cost_difference = total_spending_comparison - total_spending_home
            if cost_difference > 0:
                st.warning(f"{comparison_city} is more expensive by {cost_difference:.2f} EUR.")
            else:
                st.success(f"You would save {-cost_difference:.2f} EUR in the {comparison_city}.")

            # Prepare DataFrame for the bar chart
            bar_data = pd.DataFrame({
                "City": [home_city, comparison_city],
                "Total Spending": [total_spending_home, total_spending_comparison]
            })

            # Plot the bar chart using Streamlit's built-in bar chart function
            st.bar_chart(bar_data.set_index("City")["Total Spending"])

        except IndexError:
            st.error("Error fetching data. Please check the city selection.")