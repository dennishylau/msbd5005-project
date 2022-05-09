# IMF Direction of Trade
import plotly.graph_objects as go
from cache import dfc_imf_dot


def get_df():
    df_dot = dfc_imf_dot.query(
        '`Country Name` == "China" \
        & `Counterpart Country Name` == "United States" \
        & `Indicator Name` in ["Export", "Import"]')
    df_dot = df_dot.set_index('Indicator Name')
    df_dot = df_dot.loc[:, '1980':'2020']
    df_dot.columns = df_dot.columns.astype(int)
    df_dot = df_dot.T
    return df_dot


def get_fig_dot():
    'IMF Direction of Trade'
    df_dot = get_df()
    return (
        go.Figure(
            data=[
                go.Scatter(
                    name='Net Export',
                    x=df_dot.index,
                    y=df_dot['Export'] - df_dot['Import'],
                    opacity=0.0,
                    showlegend=False,
                    xhoverformat='%Y'),
                go.Scatter(
                    name='Export',
                    x=df_dot.index,
                    y=df_dot['Export'],
                    line_color='yellow',
                    showlegend=True,
                    xhoverformat='%Y'),
                go.Scatter(
                    name='Import',
                    x=df_dot.index,
                    y=df_dot['Import'],
                    line_color='pink',
                    showlegend=True,
                    xhoverformat='%Y',
                    text=df_dot['Export'] - df_dot['Import']),
            ],
            layout_yaxis_range=[0, 6.2e11]
        )
        .add_vline(
            x=1514764800000,  # epoch time
            line_width=3,
            line_dash='dash', line_color='cyan',
            annotation_text='2018')
        .update_xaxes(
            showticklabels=True,
            showspikes=True,
            spikedash='dash',
            spikecolor='orange',
            spikemode='toaxis+across+marker',
            type='date')
        .update_layout(
            title='China Export & Import against United States',
            height=600,
            xaxis_title='year',
            yaxis_title='$ Amount (USD)',
            hovermode='x unified'
        )
        .update_traces(hovertemplate='<br>$%{y:,.0f} USD<br>')
    )
