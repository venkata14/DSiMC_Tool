import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.io as pio
from pathlib import Path
from io import BytesIO

from src.text.instructions import instructions
from src.components.value_counts import value_counts
from src.components.histogram import histogram
from src.components.grouped import grouped
from src.components.scatter import scatter
import src.components.stats as s

# For filtering data
from src.components.filter import filter_data

# Page Details
st.set_page_config(page_title="DSiMC Tool", initial_sidebar_state="collapsed")

st.markdown("""
# DSiMC Tool

Instructions to using this tool can be found in the `Instructions` page. To get to this page, open the sidebar on the left by clicking the `>` on the top left and click on `Instructions`.

---
""")

# st.markdown(instructions)

uploaded_file = st.file_uploader("Choose a file to experiment with!", type=['csv', 'xlsx'])

if uploaded_file is not None:
    filename = Path(uploaded_file.name)
    file_type = filename.suffix
    if file_type == ".xlsx":
        df = pd.read_excel(uploaded_file)
    elif file_type == ".csv":
        df = pd.read_csv(uploaded_file)
    else:
        raise FileNotFoundError("Incorrent Type of File was uploaded.")
    st.write("Reading custom uploaded data.")
else:
    df = pd.read_excel("./sample_ehr.xlsx")
    st.write("Currently reading the sample dataset.")

# Here is the Data
st.markdown("### A quick look at the data:")
st.dataframe(df, height=200)

# list of columns
columns = df.columns.values.tolist()

# Filter Data
st.markdown("---")
st.markdown("# Filter Data")

# Individual filters require a different key for buttons, etc.
# Keep a list of the unique number id to be iterated over
# Check src.components.filter for more
if 'filter_list' not in st.session_state:
    st.session_state['filter_list'] = []
if 'filter_id' not in st.session_state:
    st.session_state['filter_id'] = 0

# Add a new filter
if st.button("Add filter", key = "add_filter_key"):
    st.session_state['filter_id'] = st.session_state.filter_id + 1
    st.session_state.filter_list.append(st.session_state.filter_id)

# Apply filters
# ***Remove function does not work***
df_filtered = filter_data(df, columns, st.session_state)

# From this point, use 'df_filtered' instead of 'df'
st.markdown("---")
st.markdown("# Choose the Type of Analysis")
analysis_option = st.selectbox(
        "Select the type of analysis",
        (None, "Value Counts", "Histogram", "Scatter Plot", "Grouped")
    )

st.markdown("---")
st.markdown("# Specify the Details")
st.markdown("""
You can specify the title of the chart under "Chart Title". You can also change the theme of the graph under "Select a Graph Theme". **Note:** you need to press "Submit" to see the updated graph after you make any changes.
""")

if analysis_option == None: 
    with st.container(border=True):
        st.write("No analysis type chosen ...")

if analysis_option == "Value Counts": value_counts(df_filtered, columns)

if analysis_option == "Histogram": histogram(df_filtered, columns)

if analysis_option == "Grouped": grouped(df_filtered, columns)

if analysis_option == "Scatter Plot": scatter(df_filtered, columns)


# -----------------------------------------------------------------

st.markdown("---")
st.markdown("# Run Statistics on you Data")
stats_option = st.selectbox(
        "Select the type of Statistics",
        (None, "Basic Statistics for Every Column", "Basic Statistics for One Column", "T-test", "Log Regression", "Chi Squared", "Paired Z-test")
    )
st.markdown("### Specify the Details")


if stats_option == "Basic Statistics for Every Column": s.summary_by_column(df_filtered)

if stats_option == "Basic Statistics for One Column": s.summary_for_one_column(df_filtered, columns)

if stats_option == "T-test": s.t_test(df_filtered, columns)

if stats_option == "Log Regression": s.log_regression(df_filtered, columns)

if stats_option == "Chi Squared": s.chi_square_test(df_filtered, columns)

if stats_option == "Paired Z-test": s.paired_z_test(df_filtered, columns)


if stats_option == None: 
    with st.container(border=True):
        st.write("No statistic options were chosen ...")
        
        


# Adding Space here
st.markdown("")

st.info("""
### _Citing this Tool:_
```
Patchigolla V., Jhand A., Lee H.J., Krishnan D., Evans M. & Li H. (2024). 
Developing Data Analytic Tools to Enhance Medical Education [Manuscript in preparation]. 
Wayne State University School of Medicine. 
https://dsimctool.streamlit.app
```

Please fill this Google form if you used this tool for a poster/presentation/publication:
https://forms.gle/YEqAdRkqzAAjXHxi8
""")
