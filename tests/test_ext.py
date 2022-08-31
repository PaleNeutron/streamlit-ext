import streamlit_ext as ste


def test_download_button():
    ste.download_button("Download", b"Hello World", "hello.txt")
