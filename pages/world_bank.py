import streamlit as st
from cache import dfc_wb_code, dfc_wb_trade, dfc_china_data


def render_wb():
    col1, col2, col3 = st.columns([1, 3, 3])
    with col1:
        st.write('# Filters')

        economies = st.multiselect(
            'Economies', dfc_wb_code.name.sort_values(),
            key='economies')
        if len(economies) == 0:
            economies = ['World']

        year_start, year_end = st.slider(
            'Select year',
            1960, 2020, (1960, 2020)
        )

    with col2:
        '## Trade (% GDP)'
        st.line_chart(dfc_wb_trade[economies].loc[year_start: year_end])

    with col3:
        st.dataframe(dfc_china_data)
