import streamlit as st
import altair as alt
from cache import dfc_china_pyramid, dfc_worldbank_gdp
from figure.pyramid import get_pyramid
from paragraphs import econ_status_1960, econ_summary_1960, demographic_1960
from streamlit.scriptrunner.script_request_queue import RerunData
from streamlit.scriptrunner.script_runner import RerunException
from streamlit_option_menu import option_menu


def percentage_difference(x, y):
    return (y - x) / x


def process_gdp(data):
    gdp = data[data['Country Code'].isin(
        ('CHN', 'JPN', "IND",))]

    gdp = gdp.melt(
        id_vars='Country Name',
        value_vars=[c for c in data.columns if c.isnumeric()],
        var_name='year',
        value_name="GDP (US$)"
    )
    gdp.loc[gdp.index, 'year'] = gdp.loc[gdp.index, 'year'].astype(int)
    return gdp


def get_gdp_series(data, min_year, max_year):
    gdp = process_gdp(data)
    gdp = gdp[
        (gdp['year'] >= min_year) &
        (gdp['year'] <= max_year)
    ]

    lines = (
        alt.Chart(gdp)
        .mark_line()
        .encode(
            x='year',
            y=alt.Y('GDP (US$):Q', axis=alt.Axis(tickCount=10, format=".1e")),
            color='Country Name:N',
            strokeDash='Country Name:N'
        )
    )
    # annotation_layer = (
    #     alt.Chart(gdp)
    #     .mark_text(size=15, text="", dx=0, dy=0, align="center")
    #     .encode(
    #         x="year",
    #         y="GDP (US$):Q",
    #         tooltip=["Country Name", "GDP (US$)"],
    #     )
    #     .interactive()
    # )
    return lines.interactive()


def get_gdp_diff(data, start_year, end_year):
    gdp = process_gdp(data)
    gdp = gdp[
        (gdp['year'] == start_year) |
        (gdp['year'] == end_year)
    ]
    gdp = gdp.set_index("year")
    gdp_diff = (
        gdp
        .groupby("Country Name")
        .apply(
            lambda x:
            percentage_difference(
                x.loc[start_year, "GDP (US$)"],
                x.loc[end_year, "GDP (US$)"]
            ) * 100
        )
        .reset_index()
    )
    gdp_diff = gdp_diff.rename({0: r"GDP % change"}, axis=1)

    bar = (
        alt.Chart(gdp_diff)
        .mark_bar(size=30)
        .encode(
            x=alt.X(r"GDP % change:Q",  scale=alt.Scale(domain=(0, 2500))),
            y='Country Name'
        )
        .properties(width=500, height=250)
    )
    return bar


def render_1960_1980():
    MIN_YEAR = 1960
    MAX_YEAR = 1980

    _, col1, _, _ = st.columns([1, 5, 5, 1])
    with col1:
        st.header("State of the Chinese economy")
    _, col1, col2, _ = st.columns([1, 5, 5, 1])
    with col1:
        st.write(econ_status_1960)
    with col2:
        gdp_chart = get_gdp_series(
            dfc_worldbank_gdp, MIN_YEAR, MAX_YEAR)
        st.altair_chart(gdp_chart, use_container_width=True)

    _, col1, col2, _ = st.columns([1, 5, 5, 1])
    with col1:
        st.write(econ_summary_1960)
    with col2:
        st.altair_chart(get_gdp_diff(dfc_worldbank_gdp, MIN_YEAR,
                        MAX_YEAR),  use_container_width=True)
    ###
    _, _, col2, _ = st.columns([1, 5, 5, 1])
    with col2:
        st.header("The human capital")
    _, col1, col2, _ = st.columns([1, 5, 5, 1])
    with col2:
        st.write(demographic_1960)
    with col1:
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
