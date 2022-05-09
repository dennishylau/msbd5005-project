import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import numpy as np
from streamlit_plotly_events import plotly_events
from cache import dfc_china_data
from utils import margin


df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
df = df[df['Country/Region'] == 'China']
df_total_death = df.iloc[:, [-1]]
df_total_death.name = 'total_death'
df_total_death = df.iloc[:, [0]].join(df_total_death)
df_total_death.columns = ['Province/State', 'total_death']

zero_mask = df_total_death['total_death'] == 0
s_total_death_log = np.log10(
    df_total_death['total_death'],
    where=np.logical_not(zero_mask))
s_total_death_log[zero_mask] = 0
df_total_death['total_death_log'] = s_total_death_log

with open('data/gadm36_CHN_1.json') as file:
    geojson = json.load(file)

fig_height = 600

fig_covid_map = (
    go.FigureWidget(go.Choropleth(
        locations=df_total_death['Province/State'],
        geojson=geojson,
        featureidkey='properties.NAME_1',
        customdata=df_total_death[['Province/State', 'total_death']],
        z=df_total_death['total_death_log'],
        colorscale='Reds',
        colorbar=dict(
            title='Total Death',
            title_font_color='white',
            tickmode='array',
            tickvals=list(range(7)),
            ticktext=[f'{x:,.0f}'
                      for x in ([0] + list(10 ** np.arange(1, 7)))],
            tickfont_color='white'
        )
    ))
    .update_layout(
        title_text='China COVID Map, Total Deaths (Updated: 2022-05-06)',
        title_font_color='white',
        height=fig_height,
        dragmode=False,
        paper_bgcolor='#101115',
        margin={'r': 0, 't': 100, 'l': 0, 'b': 90}
    )
    .update_traces(
        hovertemplate='''
        Province: %{customdata[0]}<br><br>Total Deaths: %{customdata[1]:,.0f}<br>
        <extra></extra>''',
    )
    .update_geos(
        fitbounds='locations',
        visible=False,
        bgcolor='#101116',
        projection_type='natural earth2',
    )
)


def get_df_death_ts_gp(location):
    # set default location for simplicity
    location = location if location else 'Hubei'
    df_country = df.iloc[:, 4:].sum().T
    df_city = df.query(f'`Province/State` == "{location}"').iloc[:, 4:].T
    df_death_ts = pd.concat([df_city, df_country])
    df_death_ts = df_death_ts.diff()
    df_death_ts['Date'] = pd.to_datetime(df_death_ts.index)
    df_death_ts['Date'] = df_death_ts['Date'].dt.to_period('M')
    # df_city.columns = ['Deaths', 'Date']
    df_death_ts_gp = df_death_ts.groupby('Date').sum()
    df_death_ts_gp.set_index(
        df_death_ts_gp.index.to_timestamp(how='start'),
        inplace=True)
    df_death_ts_gp.columns = ['Region Deaths', 'Country Deaths']
    df_death_ts_gp['Date'] = df_death_ts_gp.index
    return df_death_ts_gp


fig_growth = (go.Figure(
    go.Scatter(
        name='',
        x=dfc_china_data.index,
        y=dfc_china_data['GDP Growth (%)'],
        hoverinfo='x+y', xhoverformat='%Y', yhoverformat=',.2%'
    ))
    .update_xaxes(
        showspikes=True,
        spikedash='dash',
        spikecolor='orange',
        spikemode='toaxis+across+marker',
        type='date',
        range=[0, 1609459200000],  # epoch time 1970-2021
        rangeslider_visible=True,
        rangeselector_font_color='black',
        rangeselector_buttons=[
            dict(
                count=10, label='10y', step='year',
                stepmode='backward'),
            dict(
                count=20, label='20y', step='year',
                stepmode='backward'),
            dict(
                count=30, label='30y', step='year',
                stepmode='backward'),
            dict(step='all')])
    .add_vline(
        x=1577836800000,  # epoch time 2020
        line_width=3,
        line_dash='dash', line_color='cyan',
        annotation_text='2020')
    .update_yaxes(
        autorange=True,
        showspikes=True,
        spikedash='dash',
        spikecolor='orange',
        spikemode='toaxis+across+marker',
        tickformat='.0%')
    .update_layout(
        height=fig_height,
        title_text='China GDP Growth (%)',
        hovermode='x unified',
        yaxis_title='GDP Growth Rate (%)',
        xaxis_title='Year'
)
)


def render_2021():

    col11, col12 = st.columns(2)

    with col11:
        st.plotly_chart(fig_growth, use_container_width=True)

    with col12:
        margin(7)
        st.write('''
        2020 has proven to be a challenging year for China's economy. With COVID raging across different regions in, many economic activities had to stop, or could only maintain a fraction of normal capacity. Consumer spending was severely impacted across all industries, and general market outlook was negative.

        In terms of GDP growth, 2020 marked the worst performance since 1976. The line chart on the left shows the trend of GDP growth, which fell from 5.95% in 2019 to 2.30% in 2020.

        You can press one of the four range selectors at the top of the graph to select predefined time ranges, or use the range slider at the bottom of the graph to customize time range to be shown. You can also drag and select a rectangle on the graph to zoom into a particular view, and use the `Autoscale` button on the modebar, which appears upon hover, to reset the view of the graph.
        ''')

    st.write('---')

    st.write('''
    The following graphs show the COVID death numbers of China.

    The choropleth map on the left shows the total death numbers across different regions in China, with a log color scale that illustrates the numbers.

    The line graph on the right shows the number of deaths across time. You can press one of the five range selectors at the top of the graph to select predefined time ranges, or use the range slider at the bottom of the graph to customize time range to be shown.

    If you would like to explore the number of deaths across time for a specific region within China, you can click on a region in the choropleth map. The line graph on the right will then be updated to show the time series for that specific region. To reset the line graph to show numbers across al regions, click `Show Country Total` at the top right corner of the graph.
    ''')

    col21, col22 = st.columns([3, 2])

    with col21:
        selection = plotly_events(fig_covid_map, override_height=fig_height)

    with col22:
        if len(selection) >= 1 and selection[0].get('pointIndex'):
            location = df_total_death.iloc[selection[0].get(
                'pointIndex')]['Province/State']
        else:
            # location = 'Hubei'
            location = None
        print('selection', location)

        df_death_ts_gp = get_df_death_ts_gp(location)

        title_default = 'China COVID Deaths (Updated: 2022-05-06)'
        title = f'{location}, China COVID Deaths (Updated: 2022-05-06)' if location else title_default

        fig_covid_ts = (
            go.Figure()
            .add_traces(go.Scatter(
                x=df_death_ts_gp['Date'],
                y=df_death_ts_gp['Region Deaths'],
                visible=False, name='region',
                hoverinfo='x+y', xhoverformat='%B %Y'))
            .add_traces(go.Scatter(
                x=df_death_ts_gp['Date'],
                y=df_death_ts_gp['Country Deaths'],
                visible=False, name='country',
                hoverinfo='x+y', xhoverformat='%B %Y'))
            .update_layout(
                height=fig_height,
                showlegend=False,
                hovermode='x unified',
                yaxis_title='Deaths',
                xaxis_title='Date')
            .update_traces(
                line_color='red', xperiod='M1', xperiodalignment='start')
            .update_xaxes(
                showspikes=True,
                # spikesnap='data',
                spikedash='dash',
                spikecolor='orange',
                spikemode='toaxis+across+marker',
                rangeslider_visible=True,
                rangeselector_font_color='black',
                rangeselector_buttons=[
                    dict(
                        count=3, label='3m', step='month',
                        stepmode='backward'),
                    dict(
                        count=6, label='6m', step='month',
                        stepmode='backward'),
                    dict(
                        count=1, label='YTD', step='year',
                        stepmode='todate'),
                    dict(
                        count=1, label='1y', step='year',
                        stepmode='backward'),
                    dict(step='all')])
            .update_yaxes(
                rangemode='nonnegative',
                # spikesnap='data',
                showspikes=True,
                spikedash='dash',
                spikecolor='orange',
                spikemode='toaxis+across+marker')
            .update_layout(
                height=fig_height,
                showlegend=False,
                updatemenus=[
                    dict(
                        type="buttons",
                        direction="left",
                        active=0,
                        x=1,
                        xanchor="right",
                        y=1.1,
                        yanchor="top",
                        showactive=True,
                        buttons=list([
                            dict(
                                label="Show Country Total",
                                method="update",
                                args=[
                                    {"visible": [False, True]},
                                    {"title": title_default}
                                ]
                            ),
                        ]),
                        font_color='black',
                        pad={'t': 0, 'b': 0}
                    ),
                ]
            ))

        fig_covid_ts.update_layout(title_text=title)
        fig_covid_ts.for_each_trace(
            lambda trace: trace.update(visible=True)
            if trace.name == ('region' if location else 'country')
            else trace.update(visible=False)
        )
        st.plotly_chart(fig_covid_ts, use_container_width=True)
