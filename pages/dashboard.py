# %%
import streamlit as st
import numpy as np
from cache import dfc_imf_dot, dfc_worldbank_gdp
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

    country_filter, year_filter = st.columns([2, 6])

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

    gdp_indicator, import_indicator, export_indicator, trade_bal_indicator = st.columns([1, 1, 1, 1])

    with gdp_indicator:
        st.plotly_chart(plot_indicator(dfc_worldbank_gdp, chosen_year, chosen_country,
                                       indicator_name='GDP per capita (current US$)'), use_container_width=True)

    with import_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Import'), use_container_width=True)

    with export_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Export'), use_container_width=True)

    with trade_bal_indicator:
        st.plotly_chart(plot_indicator(dfc_imf_dot, chosen_year, chosen_country,
                                       indicator_name='Trade Balance'), use_container_width=True)

    data = update_data(dfc_imf_dot, chosen_country, chosen_year)

    if data.empty:
        st.markdown("<h1 style='text-align: center; color: grey;'>No trade balance data "
                    "available for the chosen country and year.</h1>", unsafe_allow_html=True)
    else:
        trade_balance_map = plot_trade_balance_map(data, chosen_country, chosen_year)

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

    if pie_chart_df[pie_chart_df['Indicator Name'] == 'Import'][str(chosen_year)].dropna().shape[0] == 1:
        st.markdown("<h3 style='text-align: center; color: grey;'>No Import data "
                    "available for the chosen country and year.</h1>", unsafe_allow_html=True)
    else:
        with pie_chart_import_plot_col:
            pie_chart_plot = plot_trade_partner_pie_chart(pie_chart_df, chosen_country, chosen_year, 'Import',
                                                          color_mapping)
            st.plotly_chart(pie_chart_plot, use_container_width=True)

    if pie_chart_df[pie_chart_df['Indicator Name'] == 'Export'][str(chosen_year)].dropna().shape[0] == 1:
        st.markdown("<h3 style='text-align: center; color: grey;'>No Export data "
                    "available for the chosen country and year.</h1>", unsafe_allow_html=True)
    else:
        with pie_chart_export_plot_col:
            pie_chart_plot = plot_trade_partner_pie_chart(pie_chart_df, chosen_country, chosen_year, 'Export',
                                                          color_mapping)
            st.plotly_chart(pie_chart_plot, use_container_width=True)
