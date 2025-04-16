"""Day 11 multiselect

Author: Bartev
Date: 2025-04-15

"""

import streamlit as st

st.title("st.multiselect")

options = st.multiselect(
    "What are your favorite colors?",
    options=["green", "yellow", "red", "blue"],
    default=["yellow", "red"],
)
options = sorted(options)
st.write(f"You selected:", options)
