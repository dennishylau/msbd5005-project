import streamlit as st


def margin(num_lines: int):
    for i in range(num_lines):  # workaround for margin
        st.write('')
