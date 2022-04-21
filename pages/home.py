# %%
import streamlit as st
import numpy as np
import altair as alt
import plotly.express as px
from cache import dfc_imf_dot, dfc_imf_map
from figure.map import plot_trade_balance_map, update_data
from streamlit_plotly_events import plotly_events
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException


def is_year(col: str) -> bool:
    """check if given string can be cast to int"""
    try:
        return bool(int(col))
    except ValueError:
        return False


YEAR_COLUMNS = [col for col in dfc_imf_dot.columns if is_year(col)]
NON_YEAR_COLUMNS = list(set(dfc_imf_dot.columns) - set(YEAR_COLUMNS))


def get_countries() -> list[str]:
    """show list of available countries to be selected by user"""
    return np.sort(dfc_imf_map['Country Name'].unique()).tolist()


def get_top_n_counterpart_countries(
        country: str,
        top_n: int = 10,
        year: int = 2021,
        trade_type: str = 'Export',
) -> list[str]:
    'Get the top n counterpart countries, ranked by trade volume'
    df = dfc_imf_dot[(dfc_imf_dot['Country Name'] == country)
                     & (dfc_imf_dot['Indicator Name'] == trade_type)]
    trade_volume = (df
                    .groupby(['Counterpart Country Name'])[str(year)]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index())
    top_n_counters = trade_volume['Counterpart Country Name'].tolist()
    top_n_counters = top_n_counters[:top_n]

    return top_n_counters


@st.experimental_memo
def get_years(chosen_country):
    """return the first and the last year that has data for a chosen country"""
    valid_years = (dfc_imf_dot[dfc_imf_dot['Country Name'] == chosen_country]
                   .loc[:, YEAR_COLUMNS]
                   .dropna(axis=1, how='all')
                   .columns)
    min_year = int(valid_years.min())
    max_year = int(valid_years.max())
    return min_year, max_year


def columns_is_in_range(column: str, min_year: int, max_year: int) -> bool:
    if column.isnumeric():
        column = int(column)
        if min_year <= column <= max_year:
            return True
        return False
    else:
        return False


def render_import_export_time_series(country, selected_years, trade_type):
    '''
    Plot import export time series using altair
    '''
    min_selected_year, max_selected_year = selected_years
    top_n_counters = get_top_n_counterpart_countries(country, 5, max_selected_year, trade_type)

    df = dfc_imf_dot[(dfc_imf_dot['Country Name'] == country)
                     & (dfc_imf_dot['Counterpart Country Name'].isin(top_n_counters))]
    num_columns = [c for c in df.columns if columns_is_in_range(c, min_selected_year, max_selected_year)]

    df = df[(df['Indicator Name'] == trade_type)]
    df = df[num_columns + ['Counterpart Country Name']].melt(
        id_vars=['Counterpart Country Name'], var_name='Year', value_name='Volume')

    line_chart = (
        alt.Chart(df, title='Trade volumns over time')
            .mark_line()
            .encode(
            x='Year',
            y='Volume',
            color='Counterpart Country Name',
            strokeDash='Counterpart Country Name',
        ).interactive())
    st.altair_chart(line_chart, use_container_width=True)


def render_trade_partner_pie_chart(
        country: str,
        selected_year: int,
        trade_type: str,
        top_n: int = 10,
):
    selected_year = str(selected_year)
    other_countries = dfc_imf_dot['Counterpart Country Name'].tolist()

    df = dfc_imf_dot[
        (dfc_imf_dot['Country Name'] == country)
        & (dfc_imf_dot['Indicator Name'] == trade_type)
        & (dfc_imf_dot['Counterpart Country Name'].isin(other_countries))
        ][['Counterpart Country Name', selected_year]]

    trade_percentage = df[selected_year].fillna(0)
    df[selected_year] = trade_percentage / trade_percentage.sum()

    df = df.sort_values(selected_year, ascending=False)

    others = df.iloc[top_n:]
    df = df.iloc[:top_n]
    df.loc[len(df)] = ['Others', others[selected_year].sum()]

    pie_chart = px.pie(df, values=selected_year,
                       names='Counterpart Country Name')

    st.plotly_chart(pie_chart, use_container_width=True)


def render_home():
    """render the page named 'home'"""

    with st.container():
        country_filter, year_filter, trade_type_filter, top_n_filter, bottom_n_filter = st.columns([2, 8, 1, 2, 2])

        if 'default_country' not in st.session_state:
            st.session_state['default_country'] = 'United States'

        st.session_state['chosen_country'] = st.session_state['default_country']

        with country_filter:
            available_countries = get_countries()
            chosen_country = st.selectbox('Country', available_countries, key='chosen_country')

        with trade_type_filter:
            chosen_trade_type = st.selectbox('Trade type', ['Export', 'Import'])

        with year_filter:
            min_year, max_year = get_years(chosen_country)
        chosen_start_year, chosen_end_year = st.slider('Year', min_year, max_year, (min_year, max_year))

        with top_n_filter:
            chosen_top_n = st.selectbox('No. of Best Profit Counterparts to Display', range(5, 11), 0)

        with bottom_n_filter:
            chosen_bottom_n = st.selectbox('No. of Worst Loss Counterparts to Display', range(5, 11), 0)

    with st.container():
        trade_balance_map, time_series_plot = st.columns([1, 1])

        with trade_balance_map:
            data = update_data(dfc_imf_map, chosen_country, chosen_start_year, chosen_end_year, chosen_top_n,
                               chosen_bottom_n)

            fig = plot_trade_balance_map(data, chosen_country, chosen_top_n, chosen_bottom_n, chosen_start_year,
                                         chosen_end_year)

            # update session_state with the country name chosen by user on the map
            chosen_points = plotly_events(fig, override_height=900, override_width="200%")
            if chosen_points:
                print(chosen_points)
                main_country = data['Country Name'].unique().tolist()
                counterpart_countries = data['Counterpart Country Name'].tolist()
                chosen_index = chosen_points[0]['pointIndex']
                if chosen_points[0]['curveNumber'] == 1:
                    st.session_state['default_country'] = counterpart_countries[chosen_index]
                    raise RerunException(RerunData())
                if chosen_points[0]['curveNumber'] == 0:
                    st.session_state['default_country'] = main_country[chosen_index]
                    raise RerunException(RerunData())

        with time_series_plot:
            render_import_export_time_series(chosen_country, (chosen_start_year, chosen_end_year), chosen_trade_type)

    with st.container():
        pie_chart_plot, _ = st.columns([1, 1])

        with pie_chart_plot:
            render_trade_partner_pie_chart(chosen_country, chosen_end_year, chosen_trade_type, )
