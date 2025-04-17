"""
Day 14 3rd party components

Author: Bartev
Date: 2025-04-16

https://streamlit.io/components

https://discuss.streamlit.io/t/streamlit-components-community-tracker/4634

"""

import pandas as pd

# import pandas_profiling
import streamlit as st
import ydata_profiling
from st_aggrid import AgGrid
from streamlit_pandas_profiling import st_profile_report
from ydata_profiling import ProfileReport

st.header("`streamlit_pandas_profiling`")

df = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv"
)

profile = ProfileReport(df, title="Profiling Report")
st_profile_report(profile)


st.subheader("AgGrid")

AgGrid(df)


df2 = pd.read_csv(
    "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
)
AgGrid(df2)
