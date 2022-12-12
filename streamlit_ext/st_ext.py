import base64
import io
import re
import uuid
from typing import Optional, Union

from streamlit.elements.button import DownloadButtonDataType

try:
    import openpyxl  # noqa: F401 # needed for pd.to_excel
    import pandas as pd
    from pandas.io.formats.style import Styler

    HAS_PD = True
except ImportError:
    HAS_PD = False

import streamlit as st

DownloadButtonDataType = Union[DownloadButtonDataType, "pd.DataFrame", "Styler"]


def set_width(width: str = "46rem") -> None:
    styl = f"""
    <style>
        .main>.block-container {{
            max-width: {width};
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)


def download_button(
    label: str,
    data: DownloadButtonDataType,
    file_name: Optional[str] = None,
    mime: Optional[str] = None,
) -> str:
    """Generates a link to download the given data, suport file-like object and pd.DataFrame.
    Params

    Args:
        button_text: text show on page.
        data: file-like object or pd.DataFrame.
        download_filename: filename and extension of file. e.g. mydata.csv,

    Raises:
        RuntimeError: when data type is not supported

    Returns:
        the anchor tag to download object_to_download

    Examples:
        download_button('Click to download data!', your_df, 'YOUR_DF.xlsx')
        download_button('Click to download text!', your_str.encode(), 'YOUR_STRING.txt')
    """

    # inspired by https://gist.github.com/chad-m/6be98ed6cf1c4f17d09b7f6e5ca2978f

    data_as_bytes: bytes
    mimetype = mime
    if isinstance(data, str):
        data_as_bytes = data.encode()
        mimetype = mimetype or "text/plain"
    elif isinstance(data, io.TextIOWrapper):
        string_data = data.read()
        data_as_bytes = string_data.encode()
        mimetype = mimetype or "text/plain"
    # Assume bytes; try methods until we run out.
    elif isinstance(data, bytes):
        data_as_bytes = data
        mimetype = mimetype or "application/octet-stream"
    elif isinstance(data, io.BytesIO):
        data.seek(0)
        data_as_bytes = data.getvalue()
        mimetype = mimetype or "application/octet-stream"
    elif isinstance(data, io.BufferedReader):
        data.seek(0)
        data_as_bytes = data.read()
        mimetype = mimetype or "application/octet-stream"
    elif isinstance(data, io.RawIOBase):
        data.seek(0)
        data_as_bytes = data.read() or b""
        mimetype = mimetype or "application/octet-stream"
    elif HAS_PD and hasattr(data, "to_excel"):
        bio = io.BytesIO()
        data.to_excel(bio)
        bio.seek(0)
        data_as_bytes = bio.read()
        mimetype = mimetype or "application/octet-stream"
    else:
        raise RuntimeError("Invalid binary data format: %s" % type(data))

    b64 = base64.b64encode(data_as_bytes).decode()
    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub(r"\d+", "", button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.4em 0.6em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgba(49, 51, 63, 0.2);
                border-image: initial;
            }}
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a class="steDownloadButton" download="{file_name}" id="{button_id}" '
        f'href="data:file/txt;base64,{b64}">{label}</a><br></br>'
    )

    div_dl_link = f"""<div class="row-widget stDownloadButton">{dl_link}</div>"""
    st.markdown(div_dl_link, unsafe_allow_html=True)
    return dl_link
