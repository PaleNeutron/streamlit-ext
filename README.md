# streamlit-ext

A small handy extension for streamlit

## Usage

### sync widgets' value with urls

When widgets value changes, the url synced and if you open the url in new tab, every value keeped.

Just import widgets from streamlit_ext, and give a specific `key` argument to it!

```python
import streamlit as st
import streamlit_ext as ste

from datetime import time, datetime, date

option = ste.selectbox(
    "How would you like to be contacted?",
    range(100),
    key="selectbox",
)

st.write("You selected:", option)

d = ste.date_input("When's your birthday", date(2019, 7, 6), key="date_input")
st.write("Your birthday is:", d)

t = ste.time_input("Set an alarm for", time(8, 45), key="time_input")
st.write("Alarm is set for", t)
```

### Download button which won't cause rerun

```python
import streamlit as st
import streamlit_ext as ste

st.title('streamlit-ext')

ste.set_page_width("60em")

ste.download_button("Download", "Hello World".encode(), "hello.txt")
```

### Set page width

```python
import streamlit as st
import streamlit_ext as ste

st.title('streamlit-ext')

ste.set_page_width("60em")

st.write("a quick fox jump..."*100)
```

## installation

```bash
pip install streamlit-ext
```
