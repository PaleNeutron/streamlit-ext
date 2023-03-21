import hashlib
import inspect
from datetime import date, datetime, time
from functools import wraps
from typing import Any, Callable, Dict, KeysView, List, Optional, Union

import streamlit as st
from packaging import version
from streamlit.runtime.state.common import GENERATED_WIDGET_ID_PREFIX

try:
    import streamlit.state.widgets as stw
except ImportError:
    import streamlit.runtime.state.widgets as stw


SYNCED_QUERY_KEYS = set()

if version.parse(st.__version__) < version.parse("1.19.0"):
    _get_widget_id_func = "_get_widget_id"
else:
    _get_widget_id_func = "compute_widget_id"

super_get_widget_id = getattr(stw, _get_widget_id_func)


def _build_sync_key(user_key: Optional[str]) -> str:
    return f"SYNC_{user_key}"


def compute_widget_id_ext(
    element_type: str, element_proto: stw.WidgetProto, user_key: Optional[str] = None
) -> str:
    synced_user_key = _build_sync_key(user_key)
    if synced_user_key in SYNCED_QUERY_KEYS:
        h = hashlib.new("md5")
        h.update(element_type.encode("utf-8"))
        # element_proto.SerializeToString contains the widget's default value
        # when default value is changed, the widget id will changed
        # and can not sync with real widget in webpage, remove it
        # h.update(element_proto.SerializeToString())
        return f"{GENERATED_WIDGET_ID_PREFIX}-{h.hexdigest()}-{synced_user_key}"
    else:
        s: str = super_get_widget_id(element_type, element_proto, user_key)
        return s


setattr(stw, _get_widget_id_func, compute_widget_id_ext)


def index2(x: Any, somelist: Union[List[Any], KeysView[Any]]) -> Optional[int]:
    somelist = list(somelist)
    return somelist.index(x) if x in somelist else None


def _trans_query_params(i: str) -> Union[str, float, datetime, date, time]:
    if i.isdigit():
        return int(i)
    elif i.replace(".", "", 1).isdigit():
        try:
            return float(i)
        except Exception:
            return i
    else:
        if ":" in i:
            try:
                return datetime.strptime(i, "%H:%M:%S").time()
            except Exception:
                pass

            try:
                return datetime.strptime(i, "%Y-%m-%d %H:%M:%S")
            except Exception:
                pass
        elif "-" in i:
            try:
                return datetime.strptime(i, "%Y-%m-%d").date()
            except Exception:
                pass
        return i


# def get_query_params():
#     params = st.experimental_get_query_params()
#     return [_trans_query_params(i) for i in params]

PARAM_TRANS_DICT: Dict[
    Callable[[Any], Any], Callable[[List[Any], Dict[str, Any]], None]
] = {}


def param_sync_builder(st_element: Callable[[Any], Any]) -> Callable[[Any], Any]:
    sig = inspect.signature(st_element)

    @wraps(st_element)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        if "key" in kwargs:
            query_label = kwargs["key"]
            params = st.experimental_get_query_params()
            bargs = sig.bind(*args, **kwargs).arguments
            # regist this key to global module，when call _get_widget_id
            # it will generate widget it without default value
            SYNCED_QUERY_KEYS.add(_build_sync_key(query_label))
            if query_label in params:
                vp_list = [_trans_query_params(i) for i in params[query_label]]
                PARAM_TRANS_DICT[st_element](vp_list, bargs)
            v = st_element(**bargs)  # type: ignore
            params.update({query_label: v})
            st.experimental_set_query_params(**params)
            return v
        else:
            return st_element(*args, **kwargs)

    return decorated


def trans_regist(st_element: Callable[[Any], Any]) -> Callable[[Any], Any]:
    def wrapper(f: Callable[[Any], None]) -> Callable[[Any], Any]:
        @wraps(f)
        def decorated(*args: Any, **kwargs: Any) -> None:
            return f(*args, **kwargs)

        PARAM_TRANS_DICT[st_element] = decorated
        pf = param_sync_builder(st_element)
        return pf

    return wrapper


@trans_regist(st.selectbox)
def selectbox(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    index = index2(v_p, bargs["options"])
    bargs["index"] = index


@trans_regist(st.radio)
def radio(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    index = index2(v_p, bargs["options"])
    bargs["index"] = index


@trans_regist(st.checkbox)
def checkbox(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    if v_p == "True":
        bargs["value"] = True
    elif v_p == "False":
        bargs["value"] = False


@trans_regist(st.multiselect)
def multiselect(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    # v_p = vp_list[0]
    bargs["default"] = vp_list


@trans_regist(st.slider)
def slider(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    # v_p = vp_list[0]
    bargs["value"] = vp_list


@trans_regist(st.select_slider)
def select_slider(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    # v_p = vp_list[0]
    if len(vp_list) == 2:
        bargs["value"] = vp_list


@trans_regist(st.text_input)
def text_input(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    bargs["value"] = v_p


@trans_regist(st.number_input)
def number_input(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    bargs["value"] = v_p


@trans_regist(st.text_area)
def text_area(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    bargs["value"] = v_p


@trans_regist(st.date_input)
def date_input(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    if len(vp_list) == 1:
        bargs["value"] = vp_list[0]
    elif len(vp_list) == 2:
        bargs["value"] = vp_list


@trans_regist(st.time_input)
def time_input(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    bargs["value"] = v_p


@trans_regist(st.color_picker)
def color_picker(vp_list: List[Any], bargs: Dict[str, Any]) -> None:
    v_p = vp_list[0]
    bargs["value"] = v_p


file_uploader = st.file_uploader
camera_input = st.camera_input
