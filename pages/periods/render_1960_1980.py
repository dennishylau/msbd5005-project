import streamlit as st
from figure.pyramid import get_pyramid
from figure.time_series import get_gdp_charts
from paragraphs import econ_status_1960_1, econ_status_1960_2, demographic_1960


def render_1960_1980(dfc_worldbank_gdp, dfc_china_data, dfc_china_pyramid):
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
                dfc_china_data,
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
