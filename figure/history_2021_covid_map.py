import plotly.graph_objects as go
import numpy as np
import json
from cache import dfc_total_death

GEOJSON_PATH = 'data/gadm36_CHN_1.json'


def get_geojson(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def get_fig_covid_map(fig_height=600):
    return (
        go.FigureWidget(
            go.Choropleth(
                locations=dfc_total_death['Province/State'],
                geojson=get_geojson(GEOJSON_PATH),
                featureidkey='properties.NAME_1',
                customdata=dfc_total_death[['Province/State', 'total_death']],
                z=dfc_total_death['total_death_log'],
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
