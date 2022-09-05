import base64
import json
import pickle
import re
import uuid
from io import BytesIO
from typing import Union

try:
    import pandas as pd

    HAS_PD = True
except ImportError:
    HAS_PD = False

import streamlit as st


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
    button_text: str,
    object_to_download: Union[bytes, "pd.DataFrame", object],
    download_filename: str,
    pickle_it: bool = False,
) -> str:
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    
    # inspired by https://gist.github.com/chad-m/6be98ed6cf1c4f17d09b7f6e5ca2978f
    
    if pickle_it:
        try:
            object_to_download = pickle.dumps(object_to_download)
        except pickle.PicklingError as e:
            st.write(e)
            return ""

    else:
        if isinstance(object_to_download, bytes):
            pass

        elif HAS_PD and isinstance(object_to_download, pd.DataFrame):
            bio = BytesIO()
            object_to_download.to_excel(bio)
            bio.seek(0)
            object_to_download = bio.read()
        # Try JSON encode for everything else
        else:
            object_to_download = json.dumps(object_to_download)

    if isinstance(object_to_download, bytes):
        b64 = base64.b64encode(object_to_download).decode()
    elif isinstance(object_to_download, str):
        b64 = base64.b64encode(object_to_download.encode()).decode()
    else:
        raise ValueError("object_to_download must be bytes or str")

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub(r"\d+", "", button_uuid)

    custom_css = f"""
        <style>
            #{button_id} {{
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: 0.25em 0.38em;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
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
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br></br>'
    )
    st.markdown(dl_link, unsafe_allow_html=True)
    return dl_link
