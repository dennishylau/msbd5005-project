import streamlit as st
from streamlit_plotly_events import plotly_events
from utils import margin
from figure.history_2021_growth import get_fig_growth
from figure.history_2021_covid_map import get_fig_covid_map
from figure.history_2021_covid_ts import get_fig_covid_ts
from cache import dfc_total_death

DESCRIBE_GDP_GROWTH = '''
        2020 has proven to be a challenging year for China's economy. With COVID raging across different regions in, many economic activities had to stop, or could only maintain a fraction of normal capacity. Consumer spending was severely impacted across all industries, and general market outlook was negative.

        In terms of GDP growth, 2020 marked the worst performance since 1976. The line chart on the left shows the trend of GDP growth, which fell from 5.95% in 2019 to 2.30% in 2020.

        You can press one of the four range selectors at the top of the graph to select predefined time ranges, or use the range slider at the bottom of the graph to customize time range to be shown. You can also drag and select a rectangle on the graph to zoom into a particular view, and use the `Autoscale` button on the modebar, which appears upon hover, to reset the view of the graph.
        '''

DESCRIBE_COVID_DEATH = '''
    The following graphs show the COVID death numbers of China.

    The choropleth map on the left shows the total death numbers across different regions in China, with a log color scale that illustrates the numbers.

    The line graph on the right shows the number of deaths across time. You can press one of the five range selectors at the top of the graph to select predefined time ranges, or use the range slider at the bottom of the graph to customize time range to be shown.

    If you would like to explore the number of deaths across time for a specific region within China, you can click on a region in the choropleth map. The line graph on the right will then be updated to show the time series for that specific region. To reset the line graph to show numbers across al regions, click `Show Country Total` at the top right corner of the graph.
    '''


def render_2021():

    col11, col12 = st.columns(2)

    with col11:
        st.plotly_chart(get_fig_growth(), use_container_width=True)

    with col12:
        margin(7)
        st.write(DESCRIBE_GDP_GROWTH)

    st.write('---')

    st.write(DESCRIBE_COVID_DEATH)

    col21, col22 = st.columns([3, 2])

    with col21:
        fig_covid_map = get_fig_covid_map()
        selection = plotly_events(fig_covid_map, override_height=600)

    with col22:
        if len(selection) >= 1 and selection[0].get('pointIndex'):
            location = dfc_total_death.iloc[selection[0].get(
                'pointIndex')]['Province/State']
        else:
            location = None
        print('selection', location)

        fig_covid_ts = get_fig_covid_ts(location)

        st.plotly_chart(fig_covid_ts, use_container_width=True)
