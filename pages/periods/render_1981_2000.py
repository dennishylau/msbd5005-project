import streamlit as st
from figure.pyramid import get_pyramid
from figure.time_series import get_gdp_charts, get_stacked_gdp_comp_area
from paragraphs import econ_status_1980_1, sector_gdp_1980_1, demographic_1980


def render_1981_2000(dfc_worldbank_gdp, dfc_china_data, dfc_china_pyramid, dfc_china_gdp_comp):
    MIN_YEAR = 1978
    MAX_YEAR = 2000
    with st.container():
        _, _, col, _, _ = st.columns([1, 1, 6, 1, 1])
        with col:
            st.header("Moderately prosperous society")
            st.markdown(econ_status_1980_1)

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
