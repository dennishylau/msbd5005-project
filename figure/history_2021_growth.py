import plotly.graph_objects as go
from cache import dfc_china_data


def get_fig_growth(fig_height=600):
    val_2020 = dfc_china_data.loc[2020, 'GDP Growth (%)']
    return (
        go.Figure(
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
            range=[0, 1577880000000],  # epoch time 1970-2020
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
            line_dash='dash', line_color='cyan')
        .add_hline(
            y=val_2020,
            line_width=3,
            line_dash='dash', line_color='cyan',
            annotation_text=f'2020: {val_2020:,.2%}',
            annotation_position='bottom right',
            annotation_bgcolor='rgba(255,255,255,1)',
            annotation_xshift=-15,
            annotation_yshift=-5,
            annotation_font_color='black')
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
