import streamlit as st
from preprocess import df_wb_code, df_wb_trade, df_imf_dot, df_imf_map


@st.experimental_memo
def __cache(obj):
    return obj


# cache
dfc_wb_code = __cache(df_wb_code)
dfc_wb_trade = __cache(df_wb_trade)
dfc_imf_dot = __cache(df_imf_dot)
dfc_imf_map = __cache(df_imf_map)
