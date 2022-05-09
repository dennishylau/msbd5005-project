import streamlit as st
import plotly.graph_objects as go
from preprocess import get_df_death_ts_gp


@st.experimental_memo
def get_fig_covid_ts(location: str, fig_height=600):
    title_default = 'China COVID Deaths (Updated: 2022-05-06)'
    title_location = f'{location}, China COVID Deaths (Updated: 2022-05-06)'
    title = title_location if location else title_default

    df_death_ts_gp = get_df_death_ts_gp(location)

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
    return fig_covid_ts
