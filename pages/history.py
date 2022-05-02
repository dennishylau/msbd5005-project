import streamlit as st
import altair as alt
import pandas as pd
from cache import dfc_china_pyramid, dfc_worldbank_gdp
from figure.pyramid import get_pyramid
from paragraphs import econ_status_1960_1, econ_status_1960_2, demographic_1960
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException
from streamlit_option_menu import option_menu


def percentage_difference(x, y):
    return (y - x) / x


def process_gdp(data, countries=('CHN', 'JPN', "IND",)):
    gdp = data[data['Country Code'].isin(countries)]
    # events = pd.DataFrame(
    #     [(year, "Great Leap Forward") for year in range(1958, 1962)] +
    #     [(year, "Cultural Revolution") for year in range(1965, 1976)] +
    #     [(1976, "TangShang Earthquake"), ],
    #     columns=['year', 'events']
    # )

    gdp = gdp.melt(
        id_vars='Country Name',
        value_vars=[c for c in data.columns if c.isnumeric()],
        var_name='year',
        value_name="GDP (US$)"
    )
    gdp.loc[gdp.index, 'year'] = gdp.loc[gdp.index, 'year'].astype(int)
    # gdp = gdp.merge(events, on='year', how='left')

    return gdp


def get_gdp_series(
    data,
    min_year,
    max_year,
    countries=('CHN', 'JPN', "IND",),
    focus_years=(1960, 1969)
):
    focus_start, focus_end = focus_years
    gdp = process_gdp(data, countries)
    gdp = gdp[
        (gdp['year'] >= min_year) &
        (gdp['year'] <= max_year)
    ]

    gdp_growth = (
        gdp
        .set_index('year')['GDP (US$)']
        .pct_change()
        .reset_index()
        .rename({'GDP (US$)': 'Annual GDP growth %'}, axis=1)
    )

    lines = (
        alt.Chart(gdp)
        .mark_line()
        .encode(
            x='year',
            y=alt.Y('GDP (US$):Q', axis=alt.Axis(tickCount=10, format=".1e")),
        )
    )

    lines_colored = (
        alt.Chart(gdp)
        .mark_line()
        .encode(
            x='year',
            y=alt.Y('GDP (US$):Q', axis=alt.Axis(tickCount=10, format=".1e")),
            color=alt.value('orange')
        )
        .transform_filter(
            (alt.datum.year >= focus_start) & (alt.datum.year <= focus_end)
        )
    )

    bar = (
        alt.Chart(gdp_growth)
        .mark_bar()
        .encode(
            x='year',
            y=alt.Y('Annual GDP growth %:Q'),
        )
    )
    bar_colored = (
        alt.Chart(gdp_growth)
        .mark_bar()
        .encode(
            x='year',
            y=alt.Y('Annual GDP growth %:Q'),
            color=alt.value("orange")
        )
        .transform_filter(
            (alt.datum.year >= focus_start) & (alt.datum.year <= focus_end)
        )
    )

    return alt.hconcat(
        lines + lines_colored,
        bar + bar_colored
    )


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

            gdp_chart = get_gdp_series(
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


MENU_NAMES = ['1960 - 1980', '1980 - 2000',
              '2000 - 2010', '2010 - 2020', '2020 - ?']


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
        generate_buttons(2)
    elif menu == MENU_NAMES[3]:
        generate_buttons(3)
    elif menu == MENU_NAMES[4]:
        return generate_buttons(4)
    return False
