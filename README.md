# streamlit-ext

[![PyPI Latest Release](https://img.shields.io/pypi/v/streamlit-ext.svg)](https://pypi.org/project/streamlit-ext/)
[![streamlit-ext-demo](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://paleneutron-streamlit-ext-testse2etest-sync-widget-orfpyh.streamlitapp.com/)

A small handy extension for streamlit, keep your widget values in url, and share it with your friends.

Use widget from `stramlit-ext` just as `streamlit` and pass a unique `key` to it!

![example gif](https://raw.githubusercontent.com/PaleNeutron/streamlit-ext/master/docs/examples.gif)

```python
import numpy as np
import pandas as pd

import streamlit as st
import streamlit_ext as ste

df = pd.DataFrame(np.random.rand(10, 5))


option = ste.selectbox(
    "A form will show up if you select less than 10",
    range(100),
    key="selectbox",
)

st.write("You selected:", option)

age = ste.slider("How old are you?", 0, 130, 25, key="slider1")
st.write("I'm ", age, "years old")

ste.download_button("Click to download data!", df, "YOUR_DF.xlsx")
ste.download_button("Click to download text!", b"text content", "YOUR_STRING.txt")
```



## installation

```bash
pip install streamlit-ext
```

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
