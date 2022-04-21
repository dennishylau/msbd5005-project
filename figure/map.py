import numpy as np
import pandas as pd
import plotly.graph_objects as go
from constants import TRADE_BAL_MAP_LINE_MAX_WIDTH, TRADE_BAL_MAP_LINE_MIN_WIDTH


def get_line_width(series: pd.Series, line_max_width: int = TRADE_BAL_MAP_LINE_MAX_WIDTH,
                   line_min_width: int = TRADE_BAL_MAP_LINE_MIN_WIDTH) -> np.array:
    """
    computes line widths the be drawn on plotly map.

    first normalize the values by dividing the values by the maximum.
    the values are then scaled to the range [LINE_MIN_WIDTH, LINE_MAX_WIDTH] while maintaining the proportions.
    :param series: pd.Series. The pandas series that the line width is based on.
    :param line_max_width: int. Defaults to 10
    :param line_min_width: int. Defaults to 1
    :return line_width_array: np.array. The numpy array of float values where each value is the line width.
    """
    normalized_values = (series / series.max()).to_numpy()
    line_width_array = ((normalized_values - np.min(normalized_values))
                        / (np.max(normalized_values) - np.min(normalized_values))
                        * (line_max_width - line_min_width) + line_min_width)
    return line_width_array


def update_data(dfc_imf_map: pd.DataFrame, chosen_country: str, chosen_start_year: int, chosen_end_year: int,
                chosen_top_n: int, chosen_bottom_n: int) -> pd.DataFrame:
    """
    given preprocessed data for plotting the trade balance map, update the data base on user filters

    :param dfc_imf_map: pd.DataFrame. Preprocessed data that is already cached.
    :param chosen_country: str. User's chosen country to display.
    :param chosen_start_year: int. User's chosen starting year.
    :param chosen_end_year: int. User's chosen ending year.
    :param chosen_top_n: int. User's chosen top N countries that the chosen country is profiting from.
    :param chosen_bottom_n: int. User's chosen bottom N countries that the chosen country is losing to.
    :return data: pd.DataFrame. Filtered dataframe ready to be plotted using plotly map.
    """
    country_data = dfc_imf_map[dfc_imf_map['Country Name'] == chosen_country].copy()

    year_columns = [str(year) for year in range(chosen_start_year, chosen_end_year + 1)]
    country_data['total'] = country_data[year_columns].sum(axis=1)

    # prepare a column named 'width' that stores the width of lines to be plotted on the map
    pos_balance = country_data[country_data['total'] >= 0].sort_values(by='total', ascending=False)
    pos_balance['width'] = get_line_width(pos_balance['total'])

    neg_balance = country_data[country_data['total'] < 0].sort_values(by='total', ascending=True)
    neg_balance['width'] = get_line_width(neg_balance['total'])

    data = pd.concat([pos_balance.head(chosen_top_n), neg_balance.head(chosen_bottom_n)], ignore_index=True)
    return data


def plot_trade_balance_map(data, chosen_country, chosen_top_n, chosen_bottom_n, chosen_start_year, chosen_end_year,
                           chosen_country_color='rgb(255, 232, 84)', counterpart_country_color='rgb(230, 230, 230)',
                           profit_color='rgb(45,237,28)', loss_color='rgb(254,2,1)', land_color='rgb(51, 51, 51)'):

    fig = go.FigureWidget()

    chosen_country_code = data['Country Code ISO3'].unique().tolist()
    chosen_country_lat = data['latitude'].iloc[0]
    chosen_country_lon = data['longitude'].iloc[0]

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
            lon=[row['longitude'], row['Counterpart longitude']],
            lat=[row['latitude'], row['Counterpart latitude']],
            mode='lines',
            line=dict(
                width=row['width'],
                color=profit_color if row['total'] >= 0 else loss_color
            ),
            hovertemplate=f'Counterpart Country: {row["Counterpart Country Name"]}<br>'
                          + row['Indicator Name'] + f': {row["total"]}<extra></extra>'))

    fig.update_traces(showlegend=False)
    fig.update_layout(
        autosize=True,
        margin=dict(
            l=0,
            r=0,
            b=50,
            t=50,
            pad=0,
            autoexpand=False),
        hoverlabel_align='right',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        template='plotly_dark',
        title_text=f"Top {chosen_top_n} & Bottom {chosen_bottom_n} Trade Balances "
                   + f"of {chosen_country} from {chosen_start_year} to {chosen_end_year}")

    fig.update_geos(
        landcolor=land_color,
        bgcolor='rgba(0,0,0,0)')

    return fig
