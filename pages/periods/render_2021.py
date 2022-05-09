import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json
import streamlit as st
import numpy as np
from streamlit_plotly_events import plotly_events
from cache import dfc_china_data


df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
df = df[df['Country/Region'] == 'China']
# df_total_death = df.loc[:, '1/22/20':].sum(axis=1)
df_total_death = df.iloc[:, [-1]]
df_total_death.name = 'total_death'
# df_total_death = df.iloc[:, [:4, -1]].join(df_total_death)
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

fig = (
    # px.choropleth(
    #     df,
    #     geojson=geojson,
    #     locations='Province/State',
    #     featureidkey='properties.NAME_1',
    #     color='total_death_log',
    #     color_continuous_scale='Reds',
    #     title='China COVID Map, Total Deaths',
    #     custom_data=df[['Province/State', 'total_death']]
    # )
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
        title_text='China COVID Map, Total Deaths',
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
    df_death_ts_gp.columns = ['City Deaths', 'Country Deaths']
    df_death_ts_gp['Date'] = df_death_ts_gp.index
    return df_death_ts_gp


fig_growth = (go.Figure(
    go.Scatter(
        name='',
        x=dfc_china_data.index,
        y=dfc_china_data['GDP Growth (%)'],
        hovertemplate='%{y:.2%}'))
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

    st.plotly_chart(fig_growth, use_container_width=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        selection = plotly_events(fig, override_height=fig_height)

    with col2:
        if len(selection) >= 1 and selection[0].get('pointIndex'):
            location = df_total_death.iloc[selection[0].get(
                'pointIndex')]['Province/State']
        else:
            # location = 'Hubei'
            location = None
        print('selection', location)

        df_death_ts_gp = get_df_death_ts_gp(location)

        y = 'City Deaths' if location else 'Country Deaths'
        title = f'{location}, China COVID Deaths' if location else 'Total China COVID Deaths'

        fig_ts = (
            px.line(
                df_death_ts_gp, x='Date', y=y,
                title=title, markers=True,
                range_x=[df_death_ts_gp.index.min(),
                         df_death_ts_gp.index.max()],
                hover_data={'Date': "|%B, %Y"}
            )
            .add_traces(go.Scatter(
                x=df_death_ts_gp['Date'],
                y=df_death_ts_gp['Country Deaths'],
                visible=False))
            .update_layout(
                height=fig_height,
                showlegend=False)
            .update_traces(
                line_color='red', xperiod='M1', xperiodalignment='start')
            .update_xaxes(
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
            .update_yaxes(rangemode='nonnegative')
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
                                    {"title": 'Total China COVID Deaths'}
                                ]
                            ),
                        ]),
                        font_color='black',
                        pad={'t': 0, 'b': 0}
                    ),
                ]
            ))
        # if location:
        #     fig_ts.update_layout(
        #         updatemenus=[
        #             dict(
        #                 type="buttons",
        #                 direction="left",
        #                 active=0,
        #                 x=1,
        #                 xanchor="right",
        #                 y=1.1,
        #                 yanchor="top",
        #                 showactive=True,
        #                 buttons=list([
        #                     dict(
        #                         label="Show Country Total",
        #                         method="update",
        #                         args=[
        #                             {"visible": [False, True]},
        #                             {"title": 'Total China COVID Deaths'}
        #                         ]
        #                     ),
        #                 ]),
        #                 font_color='black',
        #                 pad={'t': 0, 'b': 0}
        #             ),
        #         ]
        #     )
        # df_city = df_city.set_index('date')
        # df_city.columns = [f'{location} Deaths']
        # df_city = df_city.diff().dropna()
        # df_city_gp = df_city.groupby(
        #     [df_city.index.year, df_city.index.month]).sum()
        # df_city_gp.index.set_names(['year', 'month'], inplace=True)
        # df_city_gp['Month'] = df_city_gp.index.to_period('M')
        # df_city_gp = df_city_gp.set_index('Month')
        st.plotly_chart(fig_ts, use_container_width=True)
        # st.line_chart(df_city_gp, use_container_width=True, height=800)
