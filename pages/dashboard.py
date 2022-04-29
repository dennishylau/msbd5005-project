# %%
import streamlit as st
import numpy as np
from cache import dfc_imf_dot, dfc_worldbank_gdp, dfc_population_15_64_percent, dfc_wb_code
from figure.map import plot_trade_balance_map, update_data
from figure.indicator import plot_indicator
from figure.pie_chart import plot_trade_partner_pie_chart, prepare_data, prepare_color_mapping
from streamlit_plotly_events import plotly_events
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException


def is_year(col: str) -> bool:
    """Check if given string can be cast to int"""
    try:
        return bool(int(col))
    except ValueError:
        return False


YEAR_COLUMNS = [col for col in dfc_imf_dot.columns if is_year(col)]
NON_YEAR_COLUMNS = list(set(dfc_imf_dot.columns) - set(YEAR_COLUMNS))


def get_countries() -> list[str]:
    """Shows the list of available countries to be selected by user"""
    return np.sort(dfc_imf_dot['Country Name'].unique()).tolist()


@st.experimental_memo
def get_years(chosen_country):
    """Returns the first and the last year that has data for a chosen country"""
    valid_years = (dfc_imf_dot[dfc_imf_dot['Country Name'] == chosen_country]
                   .loc[:, YEAR_COLUMNS]
                   .dropna(axis=1, how='all')
                   .columns)
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())
    return min_year, max_year


def render_dashboard():
    """Renders the page named 'home'"""

    country_filter, year_filter, top_n_filter, bottom_n_filter = st.columns([2, 6, 2, 2])

    if 'default_country' not in st.session_state:
        st.session_state['default_country'] = 'China'

    st.session_state['chosen_country'] = st.session_state['default_country']

    def update_country():
        st.session_state['default_country'] = st.session_state['chosen_country']

    with country_filter:
        available_countries = get_countries()
        chosen_country = st.selectbox('Country', available_countries, key='chosen_country',
                                      on_change=update_country)

    with year_filter:
        min_year, max_year = get_years(chosen_country)
        chosen_year = st.slider('Year', min_year, max_year, 2020)

    with top_n_filter:
        chosen_top_n = st.selectbox('No. of Best Profit Counterparts to Display', range(5, 11), 0)

    with bottom_n_filter:
        chosen_bottom_n = st.selectbox('No. of Worst Loss Counterparts to Display', range(5, 11), 0)

    gdp_indicator, population_indicator, import_indicator, export_indicator, trade_bal_indicator = st.columns(
        [1, 1, 1, 1, 1])

    with gdp_indicator:
        st.plotly_chart(plot_indicator(dfc_worldbank_gdp, chosen_year, chosen_country,
                                       indicator_name='GDP per capita (current US$)'), use_container_width=True)

    with population_indicator:
        st.plotly_chart(plot_indicator(dfc_population_15_64_percent, chosen_year, chosen_country,
                                       indicator_name='Population ages 15-64 (% of total population)'),
                        use_container_width=True)

    with import_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Import'), use_container_width=True)

    with export_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Export'), use_container_width=True)

    with trade_bal_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Trade Balance'), use_container_width=True)

    data = update_data(dfc_imf_dot, chosen_country, chosen_year, chosen_top_n, chosen_bottom_n)

    trade_balance_map = plot_trade_balance_map(data, chosen_country, chosen_top_n, chosen_bottom_n, chosen_year)

    # update session_state with the country name chosen by user on the map
    chosen_points = plotly_events(trade_balance_map)
    if chosen_points:
        main_country = data['Country Name'].unique().tolist()
        counterpart_countries = data['Counterpart Country Name'].tolist()
        chosen_index = chosen_points[0]['pointIndex']
        if chosen_points[0]['curveNumber'] == 1:
            st.session_state['default_country'] = counterpart_countries[chosen_index]
            raise RerunException(RerunData())
        if chosen_points[0]['curveNumber'] == 0:
            st.session_state['default_country'] = main_country[chosen_index]
            raise RerunException(RerunData())

    pie_chart_import_plot_col, pie_chart_export_plot_col = st.columns([1, 1])

    pie_chart_df = prepare_data(dfc_imf_dot, chosen_country, chosen_year)
    color_mapping = prepare_color_mapping(pie_chart_df)

    with pie_chart_import_plot_col:
        pie_chart_plot = plot_trade_partner_pie_chart(pie_chart_df, chosen_country, chosen_year, 'Import',
                                                      color_mapping)
        st.plotly_chart(pie_chart_plot, use_container_width=True)

    with pie_chart_export_plot_col:
        pie_chart_plot = plot_trade_partner_pie_chart(pie_chart_df, chosen_country, chosen_year, 'Export',
                                                      color_mapping)
        st.plotly_chart(pie_chart_plot, use_container_width=True)
