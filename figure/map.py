import numpy as np
import pandas as pd
import plotly.graph_objects as go
from constants import TRADE_BAL_MAP_LINE_MAX_WIDTH, TRADE_BAL_MAP_LINE_MIN_WIDTH


def normalize(series: pd.Series, line_max_width: int, line_min_width: int) -> np.array:
    normalized_values = (series / series.max()).to_numpy()
    return ((normalized_values - np.min(normalized_values))
            / (np.max(normalized_values) - np.min(normalized_values))
            * (line_max_width - line_min_width) + line_min_width)


def get_line_width_mapping(series: pd.Series, line_max_width: int = TRADE_BAL_MAP_LINE_MAX_WIDTH,
                           line_min_width: int = TRADE_BAL_MAP_LINE_MIN_WIDTH) -> dict:
    """
    computes line widths the be drawn on plotly map.

    first normalize the values by dividing the values by the maximum.
    the values are then scaled to the range [LINE_MIN_WIDTH, LINE_MAX_WIDTH] while maintaining the proportions.
    :param series: pd.Series. The pandas series that the line width is based on.
    :param line_max_width: int. Defaults to 10
    :param line_min_width: int. Defaults to 1
    :return line_width_array: np.array. The numpy array of float values where each value is the line width.
    """

    pos_series = series[series >= 0].sort_values(ascending=False)
    neg_series = series[series < 0].sort_values(ascending=True)

    pos_line_width_array = normalize(pos_series, line_max_width, line_min_width)
    neg_line_width_array = normalize(neg_series, line_max_width, line_min_width)

    return {index: width for index, width in zip(list(pos_series.index) + list(neg_series.index),
                                                 np.concatenate((pos_line_width_array, neg_line_width_array)))}


def update_data(df: pd.DataFrame, chosen_country: str, chosen_year: int, chosen_top_n: int,
                chosen_bottom_n: int, trade_type: str = 'Trade Balance') -> pd.DataFrame:
    """
    given preprocessed data for plotting the trade balance map, update the data base on user filters

    :param df: pd.DataFrame. Preprocessed data that is already cached.
    :param chosen_country: str. User's chosen country to display.
    :param chosen_year: int. User's chosen year.
    :param chosen_top_n: int. User's chosen top N countries that the chosen country is profiting from.
    :param chosen_bottom_n: int. User's chosen bottom N countries that the chosen country is losing to.
    :return data: pd.DataFrame. Filtered dataframe ready to be plotted using plotly map.
    :param trade_type: str. Defaults to 'Trade Balance'. The type of data to display.
    """

    country_data = df[df['Country Name'] == chosen_country].copy()
    country_data = country_data[country_data['Indicator Name'] == trade_type]

    chosen_year = str(chosen_year)

    country_data.dropna(subset=[chosen_year], inplace=True)

    # prepare a column named 'width' that stores the width of lines to be plotted on the map
    country_data['width'] = country_data.index.map(get_line_width_mapping(country_data[chosen_year]))

    top_n = country_data.sort_values(by=chosen_year, ascending=False)
    bottom_n = country_data.sort_values(by=chosen_year, ascending=True)

    data = pd.concat([top_n.head(chosen_top_n), bottom_n.head(chosen_bottom_n)], ignore_index=True)
    return data


def plot_trade_balance_map(data, chosen_country, chosen_top_n, chosen_bottom_n, chosen_year,
                           chosen_country_color='rgb(255, 232, 84)', counterpart_country_color='rgb(230, 230, 230)',
                           profit_color='rgb(45,237,28)', loss_color='rgb(254,2,1)', land_color='rgb(51, 51, 51)'):
    fig = go.FigureWidget()

    chosen_year = str(chosen_year)
    chosen_country_code = data['Country Code ISO3'].unique().tolist()

    # add chosen country
    fig.add_traces(go.Choropleth(
        locations=chosen_country_code,
        locationmode='ISO-3',
        z=[1],
        colorscale=[[0, chosen_country_color], [1, chosen_country_color]],
        marker_line_color='white',
        marker_line_width=2,
        colorbar=None,
        showscale=False,
        hovertemplate=f'<b>{chosen_country}</b>' + f'<extra>{chosen_country_code[0]}</extra>',
        hoverlabel_bgcolor=chosen_country_color))

    # add counterpart countries
    fig.add_trace(go.Choropleth(
        locations=data['Counterpart Country Code ISO3'],
        z=[1 for _ in range(0, data['Counterpart Country Code ISO3'].shape[0])],
        locationmode='ISO-3',
        colorscale=[[0, counterpart_country_color], [1, counterpart_country_color]],
        text=data['Counterpart Country Name'],
        hovertext=data['Counterpart Country Code ISO3'],
        marker_line_color='white',
        marker_line_width=2,
        autocolorscale=False,
        showscale=False,
        hovertemplate='<b>%{text}</b><br><extra>%{hovertext}</extra>',
        hoverlabel_bgcolor=counterpart_country_color))

    for i, row in data.iterrows():
        # add lines
        fig.add_trace(go.Scattergeo(
            locationmode='ISO-3',
            locations=[row['Country Code ISO3'], row['Counterpart Country Code ISO3']],
            mode='lines',
            line=dict(
                width=row['width'],
                color=profit_color if row[chosen_year] >= 0 else loss_color
            ),
            hovertemplate=f'Counterpart Country: {row["Counterpart Country Name"]}<br>{row["Indicator Name"]}'
                          + f': {round(row[chosen_year] / 1_000_000, 2)} million US $<extra></extra>'))

    fig.update_traces(showlegend=False)
    fig.update_layout(
        autosize=True,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=50,
            pad=0,
            autoexpand=False),
        hoverlabel_align='right',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template='plotly_dark',
        title_text=f"Top {chosen_top_n} & Bottom {chosen_bottom_n} Trade Balances "
                   + f"of {chosen_country} in {chosen_year}")

    fig.update_geos(
        landcolor=land_color,
        bgcolor='rgba(0,0,0,0)')

    return fig
