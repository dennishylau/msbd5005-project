import streamlit as st
from preprocess import df_wb_code, df_wb_trade, df_imf_dot


@st.experimental_memo(persist="disk")
def cache(df):
    return df


# cache
dfc_wb_code = cache(df_wb_code)
dfc_wb_trade = cache(df_wb_trade)
dfc_imf_dot = cache(df_imf_dot)
