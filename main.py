# %%
import streamlit as st
from streamlit_option_menu import option_menu

# %% page setup & layout
st.set_page_config(layout="wide")

title_col, menu_col = st.columns([1, 1])
with title_col:
    '## MSBD5005 Project'
with menu_col:
    # workaround for vertical alignment
    ''
    menu = option_menu(
        None, ['Home', 'Dashboard', 'References'],
        icons=['house', 'globe', 'list-ul'],
        default_index=0, orientation="horizontal")
'---'

if menu == 'Dashboard':
    # call import here so cache only
    # init after calling set_page_config()
    from pages.dashboard import render_dashboard
    render_dashboard()
elif menu == 'World Bank':
    from pages.world_bank import render_wb
    render_wb()
elif menu == 'References':
    from pages import render_references
    render_references()
