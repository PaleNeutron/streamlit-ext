from functools import wraps
from typing import Any

import streamlit as st

from . import paramed_element


class DummySidebar:
    def __getattribute__(self, __name: str) -> Any:
        func = getattr(paramed_element, __name, getattr(st, __name))

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with st.sidebar:
                return func(*args, **kwargs)

        return wrapper
