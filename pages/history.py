import streamlit as st
import altair as alt
import pandas as pd
from cache import (
    dfc_china_pyramid,
    dfc_worldbank_gdp,
    dfc_worldbank_gdp_per_cap,
    dfc_china_pop,
    dfc_china_data,
    dfc_imf_dot
)
from figure.pyramid import get_pyramid
from figure.time_series import get_gdp_charts
from paragraphs import econ_status_1960_1, econ_status_1960_2, demographic_1960
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException
from streamlit_option_menu import option_menu
from pages.periods.render_2001_2010 import render_2001_2010


def render_1960_1980():
    MIN_YEAR = 1960
    MAX_YEAR = 1980

    with st.container():
        _, _, col1, _, _ = st.columns([1, 1, 6, 1, 1])
        with col1:
            st.header("State of the Chinese economy")

        _, _, col, _, _ = st.columns([1, 1, 6, 1, 1])
        with col:
            st.markdown(econ_status_1960_1, unsafe_allow_html=True)
            event_selection = st.selectbox('', [
                'Great famine: 1958-1961',
                'Cultural revolution: 1965-1975',
                'Tangshang earthquake: 1976'
            ])

            if event_selection == 'Great famine: 1958-1961':
                event_start, event_end = 1958, 1961
            elif event_selection == 'Cultural revolution: 1965-1975':
                event_start, event_end = 1965, 1975
            else:
                event_start, event_end = 1976, 1977

            gdp_chart = get_gdp_charts(
                dfc_worldbank_gdp,
                MIN_YEAR,
                MAX_YEAR,
                ["CHN"],
                (event_start, event_end)
            )

            st.altair_chart(gdp_chart,)
            st.markdown(
                econ_status_1960_2
            )

    with st.container():
        _, _, col1, _, _ = st.columns([1, 1, 6, 1, 1])
        with col1:
            st.header("The human capital")
        _, _, col1, col2, _, _ = st.columns([1, 1, 3, 3, 1, 1])
        with col1:
            st.write(demographic_1960)
        with col2:
            pyramid = get_pyramid(dfc_china_pyramid, MIN_YEAR, MAX_YEAR)
            st.altair_chart(pyramid, use_container_width=True)


MENU_NAMES = ['1960 - 1980', '1981 - 2000',
              '2001 - 2010', '2011 - 2020', '2021 - ?']


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
        render_1960_1980()
        generate_buttons(0)

    elif menu == MENU_NAMES[1]:
        generate_buttons(1)
    elif menu == MENU_NAMES[2]:
        render_2001_2010(dfc_china_data, dfc_imf_dot)
        generate_buttons(2)
    elif menu == MENU_NAMES[3]:
        generate_buttons(3)
    elif menu == MENU_NAMES[4]:
        return generate_buttons(4)
    return False
