import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load city price level data from the CSV file
@st.cache_data
def load_price_levels():
    try:
        data = pd.read_csv("europe_city_price_levels_with_rent.csv")
        data["City"] = data["City"].str.strip()  # Remove any extra whitespace
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Main Streamlit App
st.title("Enhanced Exchange Spending Calculator with Visual Aids")

# Load the city price levels
price_levels = load_price_levels()
if price_levels.empty:
    st.error("Failed to load city price level data.")
else:
    # Step 1: User selects their home city
    st.sidebar.header("Select Your Home City")
    cities = price_levels["City"].tolist()
    home_city = st.sidebar.selectbox("Select your home city:", cities)

    # Step 2: User inputs their typical monthly spending (excluding rent)
    st.sidebar.header("Enter Your Spending Details")
    monthly_spending = st.sidebar.number_input("Enter your typical monthly spending (excluding rent) in EUR:", min_value=0.0, step=0.01)

    # Step 3: User inputs the length of the exchange (in months)
    exchange_length = st.sidebar.number_input("Enter the length of your exchange (in months):", min_value=1, step=1)

    # Step 4: User selects a comparison city
    st.header("Compare Your Total Spending in Another City")
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
            st.subheader("Estimated Total Spending Breakdown")
            st.write(f"Typical Monthly Spending (including rent) in {home_city}: {total_monthly_cost_home:.2f} EUR")
            st.write(f"Adjusted Monthly Spending (including rent) in {comparison_city}: {total_monthly_cost_comparison:.2f} EUR")
            st.write(f"Total Spending for {exchange_length} months in {home_city}: {total_spending_home:.2f} EUR")
            st.write(f"Estimated Total Spending for {exchange_length} months in {comparison_city}: {total_spending_comparison:.2f} EUR")

            # Highlight savings or extra costs
            cost_difference = total_spending_comparison - total_spending_home
            if cost_difference > 0:
                st.warning(f"The comparison city is more expensive by {cost_difference:.2f} EUR.")
            else:
                st.success(f"You would save {-cost_difference:.2f} EUR in the comparison city.")

            # Bar chart for spending comparison
            fig, ax = plt.subplots()
            ax.bar(["Home City", "Comparison City"], [total_spending_home, total_spending_comparison], color=["blue", "red"])
            ax.set_ylabel("Total Spending (EUR)")
            ax.set_title("Total Spending Comparison")
            st.pyplot(fig)

        except IndexError:
            st.error("Error fetching data. Please check the city selection.")