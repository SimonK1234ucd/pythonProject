with secondSection:
            upper = st.container()
            with upper:
                [left, right] = st.columns(2)
                with left:
                    st.markdown("<p style='font-weight:bold'>Purchasing Power Calculator</p>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:14px'>This tab provides comprehensive information for a clear overview of the purchasing power of a selected currency.</p>", unsafe_allow_html=True)
            
                    check=st.radio("Select checkbox:", ["Historical Purchasing Power", "Future Purchasing Power"],key="check1")
                
                    if check=="Future Purchasing Power":
                        initial=st.number_input("Provide Initial Amount in EUR")
                        average=st.number_input("Provide Average Inflation Rate in %  (max. 20%)")
                        years=st.number_input("Provide Amount of Years  (max. 100)")

                        forprint=getPurchasingPower.getFuturePP(initial,average,years)
                        st.write(forprint)
                
                    if check=="Historical Purchasing Power":
                        with st.expander("Settings"):
                            listcountrys=[]
                            listcountrys=getPurchasingPower.getHistoricalPPlist()
                            country=st.selectbox("Please Select the country of your interest:", listcountrys, key="tab3b")
                            initial=st.number_input("Provide Amount today")
                            years=st.text_input("What year do you like to know the Purchasing Power of? (YYYY)")

                    if country:
                        data3=getChartMPV.CountryPurchasingPower(country)
                        st.write(f"Hisorical Money Purchasing Power of {country}: ")
                        st.line_chart(data3.set_index("Year"))
                    
                    if years and initial:
                        data3b=getPurchasingPower.getHistorialPPdata(country,years,initial)
                        st.write(f"The Value of {"{:.2f}".format(initial)} in {years} is {"{:.2f}".format(data3b)}") 

                with right:
                    st.markdown("<p style='font-weight:bold'>Compare Euro Historically</p>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:14px'>This tab offers statistics and graphical information on the historical performance of a selected currency against the Euro.</p>", unsafe_allow_html=True)

                    # Get the list of currencies
                    currencylistE=getreadfile.getAllCurrenciesComparedToEuro()

                    # Create two columns for side-by-side selection boxes
                    col1, col2 = st.columns(2)

                    # Box for selecting currency
                    with col1:
                        curE = st.selectbox("Select Currency to Compare", currencylistE, key = "curEtab2a")

                    # Dropdown for selecting time period (in the second column)
                    time_periods = ["YTD", "1 year", "2 years", "3 years", "5 years", "10 years", "20 years"]
                    with col2:
                        date = st.selectbox("Select Time Period", time_periods, key = "timeperioddate") 
                    
                    # Set the current date explicitly for testing or real usage
                    current_date = pd.to_datetime("2024-11-13")

                    # Determine the start date based on the selected time period
                    periods = {
                        "YTD": current_date.replace(month=1, day=1),
                        "1 year": current_date - pd.DateOffset(years=1),
                        "2 years": current_date - pd.DateOffset(years=2),
                        "3 years": current_date - pd.DateOffset(years=3),
                        "5 years": current_date - pd.DateOffset(years=5),
                        "10 years": current_date - pd.DateOffset(years=10),
                        "20 years": current_date - pd.DateOffset(years=20),
                    }
                    start_date = periods.get(date, current_date)

                    
                    # Get the historical chart data for the selected currency
                    chartplot = getcurrencychart(curE)

                    # Filter the data based on the selected time period
                    chartplot = chartplot[chartplot.index >= start_date]

                    # Display the historical chart
                    st.write(f"Historical Data of {curE} for the Selected Time Period ({date})")
                    st.line_chart(chartplot)
                    # Display currency risk assessment
                    # st.markdown("<p style='font-weight:bold; font-size:22px'>Currency Risk Assessment:</p>", unsafe_allow_html=True)
                    # display_currency_risk(curE, start_date)