"""line_chart

Author: Bartev
Date: 2025-04-14

line_chart is syntactic sugar around altair_chart
"""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from vega_datasets import data

st.header("Line chart")

rng = np.random.default_rng()
numbers = rng.lognormal(mean=2, sigma=0.5, size=(100, 3))

chart_data = pd.DataFrame(numbers, columns=["a", "b", "c"])
st.line_chart(chart_data.sort_values("c").reset_index(drop=True))
st.dataframe(chart_data)

c = (
    alt.Chart(chart_data)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)
st.altair_chart(c)

st.header("VegaLiteState")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(rng.random((20, 3)), columns=["a", "b", "c"])
df = st.session_state.data

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="a",
        y="b",
        size="c",
        color="c",
        tooltip=["a", "b", "c"],
        fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
    )
    .add_params(point_selector, interval_selector)
)
event = st.altair_chart(chart, key="alt_chart", on_select="rerun")
event

# Example  - Vega Lite chart

st.header("Vega Lite Chart")
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(rng.random((20, 3)), columns=["a", "b", "c"])

spec = {
    "mark": {"type": "circle", "tooltip": True},
    "params": [
        {"name": "interval_selection", "select": "interval"},
        {"name": "point_selection", "select": "point"},
    ],
    "encoding": {
        "x": {"field": "a", "type": "quantitative"},
        "y": {"field": "b", "type": "quantitative"},
        "size": {"field": "c", "type": "quantitative"},
        "color": {"field": "c", "type": "quantitative"},
        "fillOpacity": {
            "condition": {"param": "point_selection", "value": 1},
            "value": 0.3,
        },
    },
}

event = st.vega_lite_chart(
    st.session_state.data, spec, key="vega_chart", on_select="rerun"
)
event

st.header("element.add_rows")
st.text(
    "Concatenate a *dataframe* to the **bottom** of the `current` one. (written with st.text)"
)
st.write(
    "Concatenate a *dataframe* to the **bottom** of the `current` one. (written with st.write)"
)
st.markdown(
    "Concatenate a *dataframe* to the **bottom** of the `current` one. (written with st.markdown)"
)

ncol = 3
df1 = pd.DataFrame(rng.random((10, ncol)), columns=[f"col {i}" for i in range(ncol)])
my_table = st.dataframe(df1)

df2 = pd.DataFrame(rng.random((10, ncol)), columns=[f"col {i}" for i in range(ncol)])
my_table.add_rows(df2)

st.write("Do the same thing with charts")

my_chart = st.line_chart(df1)
my_chart.add_rows(df2)

st.subheader("vega_lite chart2")
my_chart = st.vega_lite_chart(
    {
        "mark": "line",
        "encoding": {"x": "a", "y": "b"},
        "datasets": {
            "some_fancy_name": df1,  # <-- named dataset
        },
        "data": {"name": "some_fancy_name"},
    }
)
my_chart.add_rows(some_fancy_name=df2)  # <-- name used as keyword

st.subheader("With tabs")


source = data.cars()

chart = (
    alt.Chart(source)
    .mark_circle()
    .encode(
        x="Horsepower",
        y="Miles_per_Gallon",
        color="Origin",
    )
    .interactive()
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Altair theme.
    st.altair_chart(chart, theme=None, use_container_width=True)
