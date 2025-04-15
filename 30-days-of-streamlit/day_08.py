from datetime import datetime, time

import streamlit as st

st.header("slider demo")


def run_slider():

    # Example 1

    st.header("st.slider")

    st.subheader("Slider")

    age = st.slider(label="How old are you", min_value=0, max_value=100, value=None)
    st.write(f"I'm {age} years old")

    # Example 2

    st.subheader("Range slider")

    values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
    st.write(f"Values: {values}")

    # Example 3

    st.subheader("Range time slider")
    appointment = st.slider(
        "Schedule your appointment", value=(time(11, 30), time(12, 45))
    )

    # Example 4

    st.subheader("Datetime slider")

    start_time = st.slider(
        "When do you start?",
        value=datetime(2025, 4, 1, 9, 30),
        format="ddd - yyyy-MM-DD - hh:mm",
    )
    st.write(f"Start time: {start_time}")


def run_select_slider():
    st.subheader("Select Slider")

    # Example 1

    color = st.select_slider(
        "Select a color of the rainbow",
        options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    )
    st.write(f"My favorite color is {color}")

    # Example 2
    start_color, end_color = st.select_slider(
        "Select a range of color wavelength",
        options=[
            "red",
            "orange",
            "yellow",
            "green",
            "blue",
            "indigo",
            "violet",
        ],
        value=("red", "blue"),
    )
    st.write("You selected wavelengths between", start_color, "and", end_color)


def main():

    choices = {"slider": run_slider, "select_slider": run_select_slider}
    add_sidebar = st.sidebar.selectbox("Slider command", choices, index=0)
    choices[add_sidebar]()


if __name__ == "__main__":
    main()
