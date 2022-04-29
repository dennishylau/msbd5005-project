import altair as alt
import streamlit as st
import pandas as pd
from cache import dfc_china_pyramid, dfc_china_data, dfc_china_pop
from figure.pyramid import get_pyramid


def get_gdp_series(data, min_year, max_year):
    data = data[
        (data.index >= min_year) &
        (data.index <= max_year)
    ]
    return st.line_chart(data['GDP Per Capita (US $)'])


def get_pop_growth_series(data, min_year, max_year):
    pct_change = data.pct_change()
    pct_change = pct_change[
        (pct_change.index >= min_year) &
        (pct_change.index <= max_year)
    ] * 100
    pct_change.name = r"population % change"

    return st.line_chart(pct_change)


def render_1960_1980():

    MIN_YEAR = 1960
    MAX_YEAR = 1980

    st.header("1960 - 1980")
    col1, col2 = st.columns(2)
    with col1:
        st.write(
            """
                In the years from 1960 to 1975, China was a very poor country. 
                The average GDP was aruound X dollars per capita, 
                that's just a little over Y percent of the US during
                the same time period.
                """
        )
    with col2:
        get_gdp_series(dfc_china_data, MIN_YEAR, MAX_YEAR)
    col1, col2 = st.columns(2)
    with col1:
        st.write(
            r"""
                At the beginning of the 60's, much of China's population 
                is skewed towards the young side, with over X% of the 
                being in between 0 - 15 years old. We can see a steady 
                growth in the workforce as the years go by. By the 1980's,
                China's workforce has grown to Y.

                China's large and young population can provide cost 
                competitive labour, which benefits its 
                efforts to open up its economy and in the late 70's.

                Interestingly, the Chinese Communist Party implemented the
                infamous "One Child Policy" in the year 1980. We will 
                see the policy's effects on the population and China's 
                economic future in later chapters.
            """
        )
    with col2:
        pyramid = get_pyramid(dfc_china_pyramid, MIN_YEAR, MAX_YEAR)
        st.altair_chart(pyramid, use_container_width=True)
    st.line_chart(get_pop_growth_series(dfc_china_pop, MIN_YEAR, MAX_YEAR))


def render_history():

    with st.container():
        st.title("China's economics history 1960-2020")
        col1, col2, col3, col4, col5 = st.columns(5)

        with st.container():
            with col1:
                st.button('1960-1980')
            with col2:
                st.button('1980-2000')
            with col3:
                st.button('2000-2010')
            with col4:
                st.button('2010-2020')
            with col5:
                st.button('2020-?')

        with st.container():
            render_1960_1980()
