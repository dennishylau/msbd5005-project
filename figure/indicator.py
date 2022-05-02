import pandas as pd
import plotly.graph_objects as go


def plot_indicator(df: pd.DataFrame, chosen_year: int, chosen_country: str, indicator_name: str) -> go.Figure:
    previous_year = str(chosen_year - 1)
    chosen_year = str(chosen_year)
    fig = go.Figure()

    country_data = df[df['Country Name'] == chosen_country]
    country_data = country_data[country_data['Indicator Name'] == indicator_name]
    if chosen_year not in country_data.columns:
        chosen_year_value = None
    else:
        chosen_year_value = country_data[chosen_year].values[0]

    if indicator_name.startswith('Population'):
        indicator_name = 'Population ages 15-64<br>(% of Total Population)'
    elif indicator_name.startswith('GDP'):
        indicator_name = 'GDP per capita<br>(current US$)'
    else:
        indicator_name += '<br>(US$)'

    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=chosen_year_value,
        title={"text": f"{indicator_name}"},
        delta={'reference': country_data[previous_year].values[0],
               'relative': True,
               'valueformat': '.2%'} if previous_year in country_data.columns else None))

    fig.update_layout(autosize=False,
                      width=1000,
                      height=250,
                      margin=dict(l=0, r=0, t=0, b=0))

    return fig
