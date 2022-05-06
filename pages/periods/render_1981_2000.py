import streamlit as st
from figure.pyramid import get_pyramid
from figure.time_series import get_gdp_charts, get_stacked_gdp_comp_area
from paragraphs import econ_status_1980_1, sector_gdp_1980_1, demographic_1980


def render_1981_2000(dfc_worldbank_gdp, dfc_china_data, dfc_china_pyramid, dfc_china_gdp_comp):
    MIN_YEAR = 1978
    MAX_YEAR = 2000
    with st.container():
        _, _, col1, _, _ = st.columns([1, 1, 6, 1, 1])
        with col1:
            st.header("Moderately prosperous society")

        _, _, col, _, _ = st.columns([1, 1, 6, 1, 1])
        with col:
            st.markdown(econ_status_1980_1)
            print(dfc_china_data)
            gdp_chart = get_gdp_charts(
                dfc_worldbank_gdp,
                dfc_china_data,
                MIN_YEAR,
                MAX_YEAR,
                ["CHN"],
                (0, 0)
            )

            st.altair_chart(gdp_chart,)
            st.markdown(
                sector_gdp_1980_1
            )

            st.altair_chart(
                get_stacked_gdp_comp_area(
                    dfc_china_gdp_comp,
                    MIN_YEAR,
                    MAX_YEAR
                ),
                use_container_width=True
            )

    with st.container():
        _, _, col1, _, _ = st.columns([1, 1, 6, 1, 1])
        with col1:
            st.header("One child policy")
        _, _, col1, col2, _, _ = st.columns([1, 1, 3, 3, 1, 1])
        with col1:
            st.write(demographic_1980)
        with col2:
            pyramid = get_pyramid(dfc_china_pyramid, MIN_YEAR, MAX_YEAR)
            st.altair_chart(pyramid, use_container_width=True)
