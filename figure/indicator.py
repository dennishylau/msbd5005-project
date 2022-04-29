import pandas as pd
import plotly.graph_objects as go


def plot_indicator(df: pd.DataFrame, chosen_year: int, chosen_country: str, indicator_name: str) -> go.Figure:
    previous_year = str(chosen_year - 1)
    chosen_year = str(chosen_year)
    fig = go.Figure()

    country_data = df[df['Country Name'] == chosen_country]
    country_data = country_data[country_data['Indicator Name'] == indicator_name]
    chosen_year_value = country_data[chosen_year].values()[0]

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=chosen_year_value,
        title={"text": f"{indicator_name}"},
        delta={'reference': country_data[previous_year].values()[0],
               'relative': True} if previous_year in country_data.columns() else None,
        domain={'x': [0.6, 1], 'y': [0, 1]}))

    return fig
