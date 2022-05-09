# comtrade data for treemap
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
from cache import dfc_comtrade

COLORS_TARIFF = {
    '(?)': '#2f3452',  # mix category
    'false': 'grey',  # no additional tariff
    'true': 'red'  # has tariff
}


def get_fig_goods(height=600):
    fig_goods = (
        px.treemap(
            dfc_comtrade,
            path=['Trade Flow', 'Commodity_short',
                  'Commodity_agg_4_short', 'Commodity_agg_6_short'],
            values='Trade Value (US$)', maxdepth=-1, color='tariff',
            color_discrete_map=COLORS_TARIFF,
            custom_data=dfc_comtrade
            [['Commodity_long', 'Commodity_agg_4_long',
              'Commodity_agg_6_long']],)
        .update_layout(
            title='Commodity Categories, China Export to United States',
            height=height,
            margin=dict(t=50, l=25, r=25, b=25))
        .update_traces(
            root_color='#383948', textfont=dict(color="white"),
            hoverlabel=dict(font=dict(color='white')),
            hovertemplate='<br>'.join(
                ['Category (HS 2-digit): %{customdata[0]}<br>',
                 'Subcategory (HS 4-digit): %{customdata[1]}<br>',
                 'Subcategory (HS 6-digit): %{customdata[2]}<br>',
                 'Trade Value: $%{value:,.0f} USD',
                 '<extra></extra>']))
        .update_layout(
            title_font_color='white',
            paper_bgcolor='#101116',
            showlegend=True,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.038,
                xanchor="right", x=1, font=dict(color='white'))))
    # add cutsom legends
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Categories with Additional Traiff',
            marker_color=COLORS_TARIFF['true'])
    )
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Categories without Additional Traiff',
            marker_color=COLORS_TARIFF['false'])
    )
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Mixed Categories',
            marker_color=COLORS_TARIFF['(?)'])
    )
    fig_goods.update_xaxes(visible=False)
    fig_goods.update_yaxes(visible=False)

    return fig_goods


def write_fig_goods(height=600):
    'Read the cached python obj / html to speed up loading'
    try:
        with open('cached_html/fig_goods.html') as html:
            # get cached html to speed up rendering
            components.html(html.read(), height=height)
    except FileNotFoundError:
        fig_goods = get_fig_goods(height=height)
        # write to html as cache
        fig_goods.write_html(
            file='cached_html/fig_goods.html',
            config={'displayModeBar': False})
        st.plotly_chart(
            fig_goods,
            use_container_width=True,
            config={'displayModeBar': False})
