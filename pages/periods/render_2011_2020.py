# %%
import pandas as pd
import streamlit as st
from cache import dfc_china_data, dfc_imf_dot, dfc_comtrade, pickle_cache
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from utils import margin


# %%

dfc_china_data = dfc_china_data.sort_index()
dfc_china_data = dfc_china_data.loc[1980:2021]

plots = [
    'Trade Balance (Billions of US $)',
    'Trade Balance (% of GDP)',
    'GDP Growth (%)'
]


@pickle_cache('fig_bt')
def get_fig_bt():
    'Balance of Trade'
    return (
        make_subplots(
            rows=4, cols=1,
            specs=[
                [{"rowspan": 2}],
                [None],
                [{"rowspan": 1}],
                [{"rowspan": 1}]],
            subplot_titles=plots,
            shared_xaxes=True,
            vertical_spacing=0.1)
        .update_layout(
            height=600,  # width overridden by streamlit
            title_text='China Trade Balance and GDP Growth',
            showlegend=False)
        .add_trace(go.Scatter(
            name='',
            x=dfc_china_data.index,
            y=dfc_china_data[plots[0]]))
        .add_trace(go.Scatter(
            name='',
            x=dfc_china_data.index,
            y=dfc_china_data[plots[1]]),
            row=3, col=1)
        .add_trace(go.Scatter(
            name='',
            x=dfc_china_data.index,
            y=dfc_china_data[plots[2]]),
            row=4, col=1)
        .update_yaxes(tickformat=',.0%', row=3, col=1)
        .update_yaxes(tickformat=',.0%', row=4, col=1)
        .add_vline(
            x=2018, line_width=3,
            line_dash='dash', line_color='cyan',
            annotation_text='2018')
        .update_xaxes(
            showticklabels=True,  # show x axis on all 3 plots
            showspikes=True,
            spikedash='dash',
            spikecolor='orange',
            spikemode="toaxis+across+marker")
        .update_traces(xaxis='x3')
        .update_layout(
            hovermode='x unified',
            yaxis1=dict(title_text='$ Amount (USD)'),
            xaxis3=dict(title_text='year'))
    )

# %%


# IMF Direction of Trade
df_dot = dfc_imf_dot.query(
    '`Country Name` == "China" \
    & `Counterpart Country Name` == "United States" \
    & `Indicator Name` in ["Export", "Import"]')
df_dot = df_dot.set_index('Indicator Name')
df_dot = df_dot.loc[:, '1980':'2020']
df_dot.columns = df_dot.columns.astype(int)
df_dot = df_dot.T


@pickle_cache('fig_dot')
def get_fig_dot():
    'IMF Direction of Trade'
    return (
        go.Figure(
            data=[
                go.Scatter(
                    name='Net Export',
                    x=df_dot.index,
                    y=df_dot['Export'] - df_dot['Import'],
                    opacity=0.0,
                    showlegend=False),
                go.Scatter(
                    name='Export',
                    x=df_dot.index,
                    y=df_dot['Export'],
                    line_color='yellow',
                    showlegend=True),
                go.Scatter(
                    name='Import',
                    x=df_dot.index,
                    y=df_dot['Import'],
                    line_color='pink',
                    showlegend=True,
                    text=df_dot['Export'] - df_dot['Import']),
            ],
            layout_yaxis_range=[0, 6.2e11]
        )
        .add_vline(
            x=2018, line_width=3,
            line_dash='dash', line_color='cyan',
            annotation_text='2018')
        .update_xaxes(
            showticklabels=True,
            showspikes=True,
            spikedash='dash',
            spikecolor='orange',
            spikemode="toaxis+across+marker")
        .update_layout(
            title='China Export & Import against United States',
            height=600,
            xaxis_title='year',
            yaxis_title='$ Amount (USD)',
            hovermode='x unified'
        )
        .update_traces(hovertemplate='<br>$%{y:,.0f} USD<br>')
    )
# %%


# @st.experimental_memo
@pickle_cache('fig_goods')
def get_fig_goods():
    fig_goods = (
        px.treemap(
            dfc_comtrade,
            path=[
                # 'All Trade',
                'Trade Flow', 'Commodity_short',
                'Commodity_agg_4_short', 'Commodity_agg_6_short'],
            values='Trade Value (US$)',
            maxdepth=-1,
            color='tariff',
            color_discrete_map={
                '(?)': 'grey', 'false': 'green', 'true': 'red'},
            custom_data=dfc_comtrade[
                ['Commodity_long', 'Commodity_agg_4_long', 'Commodity_agg_6_long']],
            # textinfo="label+value+percent parent+percent entry+percent root",
        )
        .update_layout(
            title='Commodity Categories, China Export to United States',
            height=600,
            margin=dict(t=50, l=25, r=25, b=25),
            # uniformtext=dict(minsize=10, mode='show'),
            # treemapcolorway=["yellow", ],
        )
        .update_traces(
            root_color='#383948',
            textfont=dict(color="white"),
            hoverlabel=dict(font=dict(color='white')),
            hovertemplate='<br>'.join([
                'Category (HS 2-digit): %{customdata[0]}<br>',
                'Subcategory (HS 4-digit): %{customdata[1]}<br>',
                'Subcategory (HS 6-digit): %{customdata[2]}<br>',
                'Trade Value: $%{value:,.0f} USD',
                '<extra></extra>']))
        .update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.038,
                xanchor="right",
                x=1
            )
        )
    )
    # add cutsom legends
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Categories with Additional Traiff',
            marker_color='red')
    )
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Categories without Additional Traiff',
            marker_color='green')
    )
    fig_goods.add_trace(
        go.Bar(
            x=[1, 3],
            y=[1, 3],
            textposition='auto',
            name='Mixed Categories',
            marker_color='grey')
    )
    fig_goods.update_xaxes(visible=False)
    fig_goods.update_yaxes(visible=False)

    return fig_goods

# %%


def render_2011_2020():
    st.write('''
    # 2018 China-US Trade War
    Since China's entry into the World Trade Organization, China's export to the United States has grown steadily and substantially, and reached a historic high at the time in 2017.

    In 2018, US President Donald Trump began setting tariffs on Chinese imports in an attempt to reduce trade deficit, and to curb alleged intellectual property piracy.

    ---
    ''')

    col11, col12 = st.columns([2, 1])

    with col11:
        st.plotly_chart(get_fig_dot(), use_container_width=True)

    with col12:
        margin(7)
        st.write('''
        The graph to the left shows the historic data of China's export and import against the United States, provided by the International Monetary Fund. From the mid-1990s, China has steadily widen its trade surplus against the United States. Note that the amount is in nominal USD, unadjusted for inflation.

        A widening trade surplus for China means a widening trade deficit for the United States, which President Donald Trump claimed will be unfavorable to the US economy.

        The Trade War had immediate effect on China's net export to the United States, which in 2019 fell by 30 billion USD year-over-year. In the short run, President Donald Trump's effort seemed to have paid off.
        ''')

    st.write('''
        The following treemap shows all categories and subcategories of commodities impacted by the Trade War. You can click a category to zoom in, and see its corresponding subcategories in more detail. Size of boxes within the treemap are proportional to the trade value for the commodity category. Red boxes indicate categories with additional tariff specific to China; green boxes indicate unimpacted categories; while grey boxes have some subcategories that were impacted, and others that were not impacted.
        ''')

    st.plotly_chart(
        get_fig_goods(),
        use_container_width=True,
        config={'displayModeBar': False})

    col21, col22 = st.columns([1, 2])

    with col21:
        margin(7)
        st.write('''
        However, when we look at the balance of trade data of China provided by the World Bank, the United States's attempt to reduce trade deficit did not devastate China's foreign trade. In fact, after a slump in trade balance in 2018, China has started recovering in 2019. China's GDP growth maintained a respectable 6% in 2019 despite the Trade War.

        In 2020, 2 years after the onset of the Trade War, China's trade balance reached historic high, while the trade balance in terms of percentage GDP remained stable. GDP Growth, however, has taken a hit from COVID-19, and was largely unrelated the remaining impact of the Trade War.
        ''')

    with col22:
        st.plotly_chart(get_fig_bt(), use_container_width=True)
