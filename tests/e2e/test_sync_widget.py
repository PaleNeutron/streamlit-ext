from datetime import date, datetime, time

import streamlit as st

import streamlit_ext as ste

option = ste.selectbox(
    "A form will show up if you select less than 10",
    range(100),
    key="selectbox",
)

st.write("You selected:", option)

sidebar_checkbox = ste.sidebar.checkbox(
    "a sidebar checkbox", value=False, key="sidebar"
)

ste.sidebar.write("sidebar selected: ", sidebar_checkbox)

if option < 10:
    with st.form("my_form"):
        st.write("Element inside a form will not sync to url until click submit buttom")
        slider_val = ste.slider("Form slider", key="form_slider")
        checkbox_val = ste.checkbox("Form checkbox", key="form_checkbox")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("slider", slider_val, "checkbox", checkbox_val)

st.write("Outside the form")

d = ste.date_input("When's your birthday", date(2019, 7, 6), key="date_input")
st.write("Your birthday is:", d)

t = ste.time_input("Set an alarm for", time(8, 45), key="time_input")
st.write("Alarm is set for", t)

agree = ste.checkbox(
    "I agree",
    key="checkbox",
)
if agree:
    st.write("Great!")

genre = ste.radio(
    "What's your favorite movie genre",
    ("Comedy", "Drama", "Documentary"),
    key="radio",
)

if genre == "Comedy":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.")

options = ste.multiselect(
    "What are your favorite colors",
    ["Green", "Yellow", "Red", "Blue"],
    ["Yellow", "Red"],
    key="multiselect",
)

st.write("You selected:", options)

# sliders

age = ste.slider("How old are you?", 0, 130, 25, key="slider1")
st.write("I'm ", age, "years old")

values = ste.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0), key="slider2")
st.write("Values:", values)

appointment = ste.slider(
    "Schedule your appointment:",
    value=(time(11, 30), time(12, 45)),
    key="slider3",
)
st.write("You're scheduled for:", appointment)

start_time = ste.slider(
    "When do you start?",
    value=datetime(2020, 1, 1, 9, 30),
    format="MM/DD/YY - hh:mm",
    key="slider4",
)
st.write("Start time:", start_time)

color = ste.select_slider(
    "Select a color of the rainbow",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    key="select_slider",
)
st.write("My favorite color is", color)

start_color, end_color = ste.select_slider(
    "Select a range of color wavelength",
    options=["red", "orange", "yellow", "green", "blue", "indigo", "violet"],
    value=("red", "blue"),
    key="select_slider2",
)
st.write("You selected wavelengths between", start_color, "and", end_color)

title = ste.text_input("Movie title", "Life of Brian", key="text_input")
st.write("The current movie title is", title)

number = ste.number_input("Insert a number", key="number")
st.write("The current number is ", number)

color = ste.color_picker("Pick A Color", "#00f900", key="color_picker")
st.write("The current color is", color)
