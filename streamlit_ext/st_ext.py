import base64
import io
import re
import uuid
from typing import TYPE_CHECKING, BinaryIO, Optional, TextIO, Union

import streamlit as st

# from streamlit.elements.widgets.button import DownloadButtonDataType

# The base type definition remains the same
DownloadButtonDataType = Union[str, bytes, TextIO, BinaryIO, io.RawIOBase]

# Now, define the extended type alias conditionally
if TYPE_CHECKING:
    import pandas as pd
    from pandas.io.formats.style import Styler

SteDownloadButtonDataType = Union[DownloadButtonDataType, "pd.DataFrame", "Styler"]


def set_width(width: str = "46rem") -> None:
    styl = f"""
    <style>
        .main>.block-container {{
            max-width: {width};
        }}
    </style>
    """
    st.markdown(styl, unsafe_allow_html=True)


LIGHT_THEME = {
    "primaryColor": "#ff4b4b",
    "backgroundColor": "#ffffff",
    "secondaryBackgroundColor": "#f0f2f6",
    "textColor": "#31333F",
    "bodyFont": '"Source Sans", sans-serif',
    "base": "light",
    "fadedText05": "rgba(49, 51, 63, 0.1)",
    "fadedText10": "rgba(49, 51, 63, 0.2)",
    "fadedText20": "rgba(49, 51, 63, 0.3)",
    "fadedText40": "rgba(49, 51, 63, 0.4)",
    "fadedText60": "rgba(49, 51, 63, 0.6)",
    "bgMix": "rgba(248, 249, 251, 1)",
    "darkenedBgMix100": "hsla(220, 27%, 68%, 1)",
    "darkenedBgMix25": "rgba(151, 166, 195, 0.25)",
    "darkenedBgMix15": "rgba(151, 166, 195, 0.15)",
    "lightenedBg05": "hsla(0, 0%, 100%, 1)",
    "font": '"Source Sans", sans-serif',
    "borderColor": "rgba(49, 51, 63, 0.2)",
}

DARK_THEME = {
    "primaryColor": "#ff4b4b",
    "backgroundColor": "#0e1117",
    "secondaryBackgroundColor": "#262730",
    "textColor": "#fafafa",
    "bodyFont": '"Source Sans", sans-serif',
    "base": "dark",
    "fadedText05": "rgba(250, 250, 250, 0.1)",
    "fadedText10": "rgba(250, 250, 250, 0.2)",
    "fadedText20": "rgba(250, 250, 250, 0.3)",
    "fadedText40": "rgba(250, 250, 250, 0.4)",
    "fadedText60": "rgba(250, 250, 250, 0.6)",
    "bgMix": "rgba(26, 28, 36, 1)",
    "darkenedBgMix100": "hsla(228, 16%, 72%, 1)",
    "darkenedBgMix25": "rgba(172, 177, 195, 0.25)",
    "darkenedBgMix15": "rgba(172, 177, 195, 0.15)",
    "lightenedBg05": "hsla(220, 24%, 10%, 1)",
    "font": '"Source Sans", sans-serif',
    "borderColor": "rgba(250, 250, 250, 0.2)",
}

THEME = {
    "light": LIGHT_THEME,
    "dark": DARK_THEME,
}


def _get_option(key: str, default: Optional[str] = None) -> Optional[str]:
    """Get a Streamlit option value, with a fallback to a default value."""
    # this function should be upgraded to use streamlit api to get theme
    # once roadmap is implemented `Python API to read active theme information`
    ret = st.get_option(key)
    if ret is None:
        theme_key = key.split(".")[-1]
        if hasattr(st.context, "theme"):
            theme_type = st.context.theme.type
        else:
            # temporary fallback for older Streamlit versions
            theme_type = "light"
        if theme_type in THEME and theme_key in THEME[theme_type]:
            return THEME[theme_type][theme_key]
        elif default is not None:
            return default
        else:
            return None
    else:
        return ret if isinstance(ret, str) else str(ret)


def download_button(
    label: str,
    data: SteDownloadButtonDataType,
    file_name: Optional[str] = None,
    mime: Optional[str] = None,
    custom_css: str = "",
) -> str:
    """Generates a link to download the given data, suport file-like object and pd.DataFrame.
    Params

    Args:
        button_text: text show on page.
        data: file-like object or pd.DataFrame.
        file_name: name of the file to be downloaded.
        mime: MIME type of the file, if not provided, will be guessed based on data type.
        custom_css: custom css to be applied to the button.


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
    elif hasattr(data, "to_excel"):
        bio = io.BytesIO()
        data.to_excel(bio)  # type: ignore
        bio.seek(0)
        data_as_bytes = bio.read()
        mimetype = mimetype or "application/octet-stream"
    else:
        raise RuntimeError("Invalid binary data format: %s" % type(data))

    b64 = base64.b64encode(data_as_bytes).decode()
    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub(r"\d+", "", button_uuid)
    primaryColor = _get_option("theme.primaryColor")
    backgroundColor = _get_option("theme.backgroundColor")
    borderColor = _get_option("theme.borderColor", "rgba(49, 51, 63, 0.2)")
    textColor = _get_option("theme.textColor")
    button_css = f"""
<style>
    #{button_id} {{
        background-color: {backgroundColor};
        color: {textColor};
        padding: 0.5em 0.5em;
        min-height: 2.5rem;
        margin-bottom: 1rem;
        display: inline-block;
        position: relative;
        text-decoration: none;
        border-radius: 0.5rem;
        border-width: 1px;
        border-style: solid;
        border-color: {borderColor};
        border-image: initial;{custom_css}
    }}
    #{button_id}:hover {{
        border-color: {primaryColor};
        color: {primaryColor};
    }}
    #{button_id}:active {{
        box-shadow: none;
        background-color: {primaryColor};
        color: white;
        }}
</style>"""

    dl_link = (
        button_css + "\n" + f"<div>"
        f'<a  class="steDownloadButton" download="{file_name}" id="{button_id}" '
        f' href="data:file/txt;base64,{b64}">{label}</a></div>'
    )

    div_dl_link = f"""<div class="row-widget stDownloadButton">\n{dl_link}\n</div>"""
    st.markdown(div_dl_link, unsafe_allow_html=True)
    return dl_link
