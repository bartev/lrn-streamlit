import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid

st.title("Hello world!")


# st.header("_Streamlit_ is :blue[cool] :sunglasses:")
# st.header("This is a header with a divider", divider="gray")
st.header("These headers have rotating dividers", divider=True)
st.header("One", divider="rainbow")
# st.header("Two", divider=True)
# st.header("Three", divider=True)
# st.header("Four", divider=True)

st.markdown("This is created with `st.markdown`")

with st.sidebar:
    st.header("About app")
    st.write("This is my 2nd app")

col1, col2 = st.columns(2)

with col1:
    x = st.slider("Choose an x value, 1, 10")
with col2:
    st.write("The value of :red[***x***] is", x)
#
# st.badge("New")
# st.badge("Success", icon=":material/check:", color="green")
#
# st.markdown(":streamlit:")
# st.markdown(
#     ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
# )
#
#
# # st.help(pandas.DataFrame.map)
#
# st.html(
#     "<p><span style='text-decoration: line-through double red;'>Oops - there it is</span>!</p>"
# )
#
#
# df = pd.read_csv(
#     "https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv"
# )
#
# AgGrid(df)


chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.area_chart(chart_data)
