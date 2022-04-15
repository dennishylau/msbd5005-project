import streamlit as st
from cache import dfc_imf_dot


def render_home():
    source = 'Australia'
    destination = 'India'

    st.dataframe(
        dfc_imf_dot.query(
            f"`Country Name` == '{source}' and `Counterpart Country Name` == '{destination}'"))
