# %%
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException

# %% page setup & layout
st.set_page_config(page_title='MSBD5005 Project', layout="wide")

title_col, menu_col = st.columns([1, 1])
with title_col:
    '## MSBD5005 Project'

MAIN_MENU_NAMES = ['The Economic Rise of China', 'Dashboard', 'References']
if 'chosen_page' not in st.session_state:
    st.session_state['chosen_page'] = MAIN_MENU_NAMES[0]

with menu_col:
    # workaround for vertical alignment
    ''
    menu = option_menu(
        None, MAIN_MENU_NAMES,
        icons=['graph-up-arrow', 'bar-chart-line', 'list-ul'],
        default_index=MAIN_MENU_NAMES.index(st.session_state['chosen_page']), orientation="horizontal")
'---'

if menu == 'Dashboard':
    # call import here so cache only
    # init after calling set_page_config()
    from pages.dashboard import render_dashboard
    del st.session_state['chosen_page']
    render_dashboard()
elif menu == 'The Economic Rise of China':
    from pages.history import render_history
    if render_history():
        st.session_state['chosen_page'] = 'Dashboard'
        raise RerunException(RerunData())
elif menu == 'References':
    from pages import render_references
    render_references()
