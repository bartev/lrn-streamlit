"""Day 5 of 30 days of streamlit

Author: Bartev
Date: 2025-04-13

https://30days.streamlit.app/?challenge=Day5

The `st.write` command
"""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.header("st.write")


# Example 1

st.write("Hello, *World!* 😎")

# Example 2

st.write(1234)

# Example 3

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
st.write(df)

# Example 4

st.write("Below is a DataFrame:", df, "Above is a dataframe")

# Example 5
rng = np.random.default_rng()
data = rng.standard_normal((200, 3))

df2 = pd.DataFrame(data, columns=["a", "b", "c"])
c = (
    alt.Chart(df2)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)
st.write(c)

st.markdown(body="Hello :flag-am:, are you 👍 there?")
st.markdown(":streamlit: -> hello -- <= <- -=")

st.write("Google Material Symbols")
st.markdown(
    ":material/fingerprint: see https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded"
)

st.markdown(":blue[Hello], :small[:red[Goodbye]], :red-background[So long]")

st.markdown(
    ":green-badge[Badger] :red-badge[Badger] :grey-badge[Badger] :blue-badge[Badger]"
)
st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown(
    """
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text."""
)
st.markdown(
    "Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:"
)

multi = """If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
"""
st.markdown(multi)

st.header(body="Headers! :balloon:", divider=True)

st.header("_Streamlit_ is :blue[cool] :sunglasses:")
st.header("This is a header with a divider", divider="gray")
st.header("These headers have rotating dividers", divider=True)
st.header("One", divider=True)
st.header("Two", divider=True)
st.header("Three", divider=True)
st.header("Four", divider=True)

st.subheader(body="Subheaders! 🎈")

st.caption("This is a string that explains something above.")
st.caption("A caption with _italics_ :blue[colors] and emojis :sunglasses:")


st.latex(
    r"""
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    """
)


code = """def hello():
    print("Hello, Streamlit!")"""
st.code(code, language="python", line_numbers=True)


st.badge("New")
st.badge("Success", icon=":material/check:", color="green")

st.markdown(
    ":violet-badge[:material/star: Favorite] :orange-badge[⚠️ Needs review] :gray-badge[Deprecated]"
)
