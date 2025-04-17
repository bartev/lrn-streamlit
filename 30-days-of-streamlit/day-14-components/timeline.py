"""Create a timeline

See examples here
https://visjs.github.io/vis-timeline/examples/timeline/

"""

from datetime import datetime

import streamlit as st
from streamlit_timeline import st_timeline

st.set_page_config(layout="wide")

items = [
    {"id": 1, "content": "2022-10-20", "start": "2022-10-20", "end": "2022-10-30"},
    {"id": 2, "content": "2022-10-09", "start": "2022-10-09"},
    {"id": 3, "content": "2022-10-18", "start": "2022-10-18"},
    {"id": 4, "content": "2022-10-16", "start": "2022-10-16"},
    {"id": 5, "content": "2022-10-25", "start": "2022-10-25"},
    {"id": 6, "content": "2022-10-27", "start": "2022-10-27"},
]

timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)

bday_dict = {
    "hilda": "10-29",
    "bartev": "11-24",
    "zareh": "07-01",
    "adrine": "01-26",
    "areg": "07-27",
}

current_year = datetime.now().year

bdays = [
    {"id": idx, "start": f"{current_year}-{date}", "content": f"{name}\n{date}"}
    for idx, (name, date) in enumerate(bday_dict.items())
]


st.subheader("Birthdays")
birthdays = st_timeline(bdays, groups=[], options={}, height="200px")
st.write(birthdays)
