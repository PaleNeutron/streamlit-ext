import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.append(Path(__file__).parents[3])

import streamlit_ext as ste  # noqa: E402

df = pd.DataFrame(np.random.rand(10, 5))


ste.download_button("Click to download data!", df, "YOUR_DF.xlsx")
ste.download_button("Click to download text!", b"text content", "YOUR_STRING.txt")
