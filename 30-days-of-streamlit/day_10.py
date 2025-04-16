"""Day 10 selectbox

Author: Bartev
Date: 2025-04-15

st.selectbox allows the display of a select widget.


A simple app that asks the user what their favorite color is.

Flow of the app:

User selects a color
App prints out the selected color

"""

import streamlit as st

st.title("st.selectbox")

st.markdown(":red[this text] was :red-background[red]")

option = st.selectbox(
    "What is your favorite color?",
    ["Blue", "Red", "Green"],
    help="Here's some random help text",
    placeholder="Bwahhhaaa",
    index=None,
)
st.write(
    f"Your favorite color is :{option.lower() if option else 'gray'}-background[{option}]"
)
