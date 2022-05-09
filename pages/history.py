import streamlit as st
import altair as alt
import pandas as pd
from cache import (
    dfc_china_pyramid,
    dfc_worldbank_gdp,
    dfc_worldbank_gdp_per_cap,
    dfc_china_pop,
    dfc_china_gdp_comp,
    dfc_china_data,
    dfc_imf_dot
)
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException
from streamlit_option_menu import option_menu
from pages.periods.render_2001_2010 import render_2001_2010
from pages.periods.render_1960_1980 import render_1960_1980
from pages.periods.render_1981_2000 import render_1981_2000


MENU_NAMES = ['1960 - 1980', '1981 - 2000',
              '2001 - 2010', '2011 - 2020', '2021 - Present']


def next_button_callback(menu_name):
    current_index = MENU_NAMES.index(menu_name)
    return MENU_NAMES[current_index + 1]


def generate_buttons(current_index):
    _, back_col, next_col = st.columns([10, 1, 11])

    if current_index > 0:
        with back_col:
            if st.button('Back'):
                st.session_state['timeline_page'] = MENU_NAMES[current_index - 1]
                raise RerunException(RerunData())

    if current_index < len(MENU_NAMES) - 1:
        with next_col:
            if st.button('Next'):
                st.session_state['timeline_page'] = MENU_NAMES[current_index + 1]
                raise RerunException(RerunData())

    if current_index == len(MENU_NAMES) - 1:
        with next_col:
            if st.button('Explore dashboard'):
                del st.session_state['timeline_page']
                return True


def render_history():
    if 'timeline_page' not in st.session_state:
        st.session_state['timeline_page'] = MENU_NAMES[0]

    menu = option_menu(
        None, MENU_NAMES,
        icons=['calendar', 'calendar', 'calendar', 'calendar', 'calendar'],
        default_index=MENU_NAMES.index(st.session_state['timeline_page']), orientation="horizontal")

    if menu == MENU_NAMES[0]:
        render_1960_1980(dfc_worldbank_gdp, dfc_china_data, dfc_china_pyramid)
        generate_buttons(0)

    elif menu == MENU_NAMES[1]:
        render_1981_2000(
            dfc_worldbank_gdp,
            dfc_china_data,
            dfc_china_pyramid,
            dfc_china_gdp_comp
        )
        generate_buttons(1)
    elif menu == MENU_NAMES[2]:
        render_2001_2010(dfc_china_data, dfc_imf_dot)
        generate_buttons(2)
    elif menu == MENU_NAMES[3]:
        from pages.periods.render_2011_2020 import render_2011_2020
        render_2011_2020()
        return generate_buttons(3)
    elif menu == MENU_NAMES[4]:
        from pages.periods.render_2021 import render_2021
        render_2021()
        return generate_buttons(4)
    return False
