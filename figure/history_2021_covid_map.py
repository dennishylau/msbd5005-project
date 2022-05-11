import plotly.graph_objects as go
import numpy as np
import json
from cache import dfc_total_death
from preprocess.china_covid import BIN_CUTS, BIN_IDX

GEOJSON_PATH = 'data/gadm36_CHN_1.json'
BIN_LABELS = [f'{BIN_CUTS[x]} - {BIN_CUTS[x+1] - 1}' for x in BIN_IDX]


def get_geojson(path):
    with open(path, encoding='utf-8') as file:
        return json.load(file)


def discrete_colorscale(bins, colors):
    if len(bins) != len(colors) + 1:
        raise ValueError(
            'len(boundary values) should be equal to len(colors)+1')
    bins = sorted(bins)
    nvals = np.linspace(0, 1, len(BIN_CUTS) - 1)
    dcolorscale = []
    for k in range(len(colors) - 1):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k + 1], colors[k]]])
    return dcolorscale


def get_fig_covid_map(fig_height=600):
    colorscale = discrete_colorscale(
        BIN_CUTS,
        ['#5AFF33', '#C0FF33', '#FFC300',
         '#FF5733', '#FF0000', '#5F1616', '#161616'])
    tickvals = [np.mean(BIN_IDX[k: k + 2])
                for k in range(len(BIN_IDX) - 1)]
    return (
        go.FigureWidget(
            go.Choropleth(
                locations=dfc_total_death['Province/State'],
                geojson=get_geojson(GEOJSON_PATH),
                featureidkey='properties.NAME_1',
                customdata=dfc_total_death[['Province/State', 'total_death']],
                z=dfc_total_death['total_death_binned'],
                colorscale=colorscale,
                colorbar=dict(
                    title='Total Death',
                    title_font_color='white',
                    tickmode='array',
                    tickvals=tickvals,
                    ticktext=BIN_LABELS,
                    tickfont_color='white',
                )
            )
        )
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
