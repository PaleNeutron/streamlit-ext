# streamlit-ext

A small handy extension for streamlit

e.g. download button which won't cause rerun, set page width function, etc.

```python
import streamlit as st
import streamlit_ext as ste

st.title('streamlit-ext')

ste.set_page_width("60em")

ste.download_button("Download", "Hello World".encode(), "hello.txt")
```

## installation

```bash
pip install streamlit-ext
```
