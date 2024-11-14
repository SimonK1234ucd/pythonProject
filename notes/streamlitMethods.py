# Streamlit Text Display
st.text()           # Display fixed-width text.
st.markdown()       # Display text with Markdown formatting.
st.title()          # Display a title (largest header).
st.header()         # Display a header (second largest).
st.subheader()      # Display a subheader.
st.caption()        # Display small caption text.
st.code()           # Display code with syntax highlighting.
st.latex()          # Display a LaTeX expression.
st.write()          # Display any object intelligently.

# Streamlit Data Display
st.dataframe()      # Display a dataframe with interactivity.
st.table()          # Display a static table.
st.json()           # Display a JSON object.
st.metric()         # Display a metric with optional delta.

# Streamlit Media Display
st.image()          # Display an image.
st.audio()          # Display an audio player.
st.video()          # Display a video player.

# Streamlit Widgets (User Input)
st.button()         # Display a button.
st.checkbox()       # Display a checkbox.
st.radio()          # Display radio buttons for single-choice selection.
st.selectbox()      # Display a dropdown for single-choice selection.
st.multiselect()    # Display a dropdown for multiple-choice selection.
st.slider()         # Display a slider for numeric values.
st.select_slider()  # Display a slider with custom options.
st.text_input()     # Display a single-line text input box.
st.text_area()      # Display a multi-line text input box.
st.number_input()   # Display a numeric input box.
st.date_input()     # Display a date picker.
st.time_input()     # Display a time picker.
st.file_uploader()  # Display a file uploader.
st.color_picker()   # Display a color picker.

# Streamlit Control Flow (Conditional Display)
st.form()           # Group inputs into a form.
st.form_submit_button() # Add a submit button to a form.
st.expander()       # Create an expandable container.

# Streamlit Charts and Graphs
st.line_chart()     # Display a line chart.
st.area_chart()     # Display an area chart.
st.bar_chart()      # Display a bar chart.
st.pyplot()         # Display a Matplotlib figure.
st.altair_chart()   # Display an Altair chart.
st.vega_lite_chart() # Display a Vega-Lite chart.
st.plotly_chart()   # Display a Plotly figure.
st.bokeh_chart()    # Display a Bokeh figure.
st.pydeck_chart()   # Display a PyDeck map.
st.map()            # Display a map using lat/lon data.

# Streamlit Status and Progress
st.progress()       # Display a progress bar.
st.spinner()        # Display a temporary spinner.
st.success()        # Display a success message.
st.error()          # Display an error message.
st.warning()        # Display a warning message.
st.info()           # Display an informational message.
st.exception()      # Display an exception traceback.

# Streamlit Layouts and Containers
st.container()      # Group elements together.
st.columns()        # Create columns for side-by-side layout.
st.sidebar()        # Display elements in a sidebar.
st.empty()          # Reserve space for other elements.
st.tabs()           # Create tabs for organizing content.
st.expander()       # Create an expandable section.

# Streamlit Experimental and Advanced
st.session_state    # Manage session state across app reruns.
st.experimental_memo() # Cache function results for speed.
st.experimental_singleton() # Cache objects initialized once.
st.experimental_data_editor() # Interactive table for editing.
st.experimental_rerun() # Manually trigger a rerun of the app.
st.experimental_show() # Show information about an object (for debugging).
