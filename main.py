# %%
import streamlit as st
from streamlit_option_menu import option_menu

# %% page setup & layout
st.set_page_config(layout="wide")

title_col, menu_col = st.columns([1, 1])
with title_col:
    '# MSBD5005 Project'
with menu_col:
    # workaround for vertical alignment
    ''
    ''
    menu = option_menu(
        None, ['Home', 'World Bank', 'References'],
        icons=['house', 'globe', 'list-ul'],
        default_index=0, orientation="horizontal")
'---'

if menu == 'Home':
    # call import here so cache only
    # init after calling set_page_config()
    from pages.home import render_home
    render_home()
elif menu == 'World Bank':
    from pages.world_bank import render_wb
    render_wb()
elif menu == 'References':
    from pages import render_references
    render_references()
