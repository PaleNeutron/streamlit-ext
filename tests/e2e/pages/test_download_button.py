import numpy as np
import pandas as pd
import streamlit as st

import streamlit_ext as ste

df = pd.DataFrame(np.random.rand(10, 5))


ste.download_button("Click to download data!", df, "YOUR_DF.xlsx")
ste.download_button("Click to download text!", b"text content", "YOUR_STRING.txt")
st.download_button("Click to download text!", b"text content", "YOUR_STRING.txt")
