# history 2011 balance of trade figure
from cache import dfc_china_data
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def get_df():
    df = dfc_china_data.copy()
    df = df.sort_index()
    df = df.loc[1980:2021]
    return df


PLOTS = [
    'Trade Balance (Billions of US $)',
    'Trade Balance (% of GDP)',
    'GDP Growth (%)'
]


def get_fig_bt():
    'Balance of Trade'
    df = get_df()
    return (
        make_subplots(
            rows=4, cols=1,
            specs=[
                [{"rowspan": 2}],
                [None],
                [{"rowspan": 1}],
                [{"rowspan": 1}]],
            subplot_titles=PLOTS,
            shared_xaxes=True,
            vertical_spacing=0.1)
        .update_layout(
            height=600,  # width overridden by streamlit
            title_text='China Trade Balance and GDP Growth',
            showlegend=False)
        .add_trace(go.Scatter(
            name='',
            x=df.index,
            y=df[PLOTS[0]],
            xhoverformat='%Y',
            hovertemplate='%{y}'))
        .add_trace(go.Scatter(
            name='',
            x=df.index,
            y=df[PLOTS[1]],
            xhoverformat='%Y',
            hovertemplate='%{y:,.2%}'),
            row=3, col=1)
        .add_trace(go.Scatter(
            name='',
            x=df.index,
            y=df[PLOTS[2]],
            xhoverformat='%Y',
            hovertemplate='%{y:,.2%}'),
            row=4, col=1)
        .update_yaxes(tickformat=',.0%', row=3, col=1)
        .update_yaxes(tickformat=',.0%', row=4, col=1)
        .update_xaxes(
            showticklabels=True,  # show x axis on all 3 plots
            showspikes=True,
            spikedash='dash',
            spikecolor='orange',
            spikemode='toaxis+across+marker',
            type='date')
        .add_vline(
            x=1514764800000,  # epoch time
            line_width=3,
            line_dash='dash', line_color='cyan',
            annotation_text='2018')
        .update_traces(xaxis='x3')
        .update_layout(
            hovermode='x unified',
            yaxis1=dict(title_text='$ Amount (USD)'),
            xaxis3=dict(title_text='year'))
    )
