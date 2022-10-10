import streamlit as st
from typing import Any, Callable, Dict, List, Optional, Union
from functools import wraps

from . import paramed_element

class DummySidebar(object):
    def __getattribute__(self, __name: str) -> Any:
        func = getattr(paramed_element, __name, getattr(st, __name))
        @wraps(func)
        def wrapper(*args, **kwargs):
            with st.sidebar:
                return func(*args, **kwargs)
        return wrapper