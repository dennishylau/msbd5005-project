import altair as alt
import pandas as pd


def columns_is_in_range(column: str, min_year: int, max_year: int) -> bool:
    if column.isnumeric():
        column = int(column)
        if min_year <= column <= max_year:
            return True
    return False


def get_top_n_counterpart_countries(dfc_imf_dot: pd.DataFrame, country: str, top_n, year: int = 2021,
                                    trade_type: str = 'Export') -> list[str]:
    """Get the top n counterpart countries, ranked by trade volume"""
    df = dfc_imf_dot[(dfc_imf_dot['Country Name'] == country)
                     & (dfc_imf_dot['Indicator Name'] == trade_type)]
    trade_volume = (df
                    .groupby(['Counterpart Country Name'])[str(year)]
                    .sum()
                    .sort_values(ascending=False)
                    .reset_index())
    top_n_counters = trade_volume['Counterpart Country Name'].tolist()
    top_n_counters = top_n_counters[:top_n]

    return top_n_counters


def plot_import_export_time_series(dfc_imf_dot, country, selected_years, trade_type, top_n: int = 10):
    """Plot import export time series using altair"""
    min_selected_year, max_selected_year = selected_years
    top_n_counters = get_top_n_counterpart_countries(dfc_imf_dot, country, top_n, max_selected_year, trade_type)

    df = dfc_imf_dot[(dfc_imf_dot['Country Name'] == country)
                     & (dfc_imf_dot['Counterpart Country Name'].isin(top_n_counters))]
    num_columns = [c for c in df.columns if columns_is_in_range(c, min_selected_year, max_selected_year)]

    df = df[(df['Indicator Name'] == trade_type)]
    df = df[num_columns + ['Counterpart Country Name']].melt(
        id_vars=['Counterpart Country Name'], var_name='Year', value_name='Volume')

    line_chart = (alt.Chart(df, title='Trade volumns over time')
                  .mark_line()
                  .encode(x='Year',
                          y='Volume',
                          color='Counterpart Country Name',
                          strokeDash='Counterpart Country Name')
                  .interactive())
    return line_chart


def percentage_difference(x, y):
    return (y - x) / x


def process_gdp(data, countries=('CHN', 'JPN', "IND",)):
    gdp = data[data['Country Code'].isin(countries)]

    gdp = gdp.melt(
        id_vars='Country Name',
        value_vars=[c for c in data.columns if c.isnumeric()],
        var_name='year',
        value_name="GDP (US$)"
    )
    gdp.loc[gdp.index, 'year'] = gdp.loc[gdp.index, 'year'].astype(int)

    return gdp


def get_gdp_charts(
    data,
    min_year,
    max_year,
    countries=('CHN', 'JPN', "IND",),
    focus_years=(1960, 1969)
):
    focus_start, focus_end = focus_years
    gdp = process_gdp(data, countries)
    gdp = gdp[
        (gdp['year'] >= min_year) &
        (gdp['year'] <= max_year)
    ]

    gdp_growth = (
        gdp
        .set_index('year')['GDP (US$)']
        .pct_change()
        .reset_index()
        .rename({'GDP (US$)': 'Annual GDP growth %'}, axis=1)
    )

    lines = (
        alt.Chart(gdp)
        .mark_line()
        .encode(
            x='year',
            y=alt.Y('GDP (US$):Q', axis=alt.Axis(tickCount=10, format=".1e")),
        )
    )

    lines_colored = (
        alt.Chart(gdp)
        .mark_line()
        .encode(
            x='year',
            y=alt.Y('GDP (US$):Q', axis=alt.Axis(tickCount=10, format=".1e")),
            color=alt.value('orange')
        )
        .transform_filter(
            (alt.datum.year >= focus_start) & (alt.datum.year <= focus_end)
        )
    )

    bar = (
        alt.Chart(gdp_growth)
        .mark_bar()
        .encode(
            x='year',
            y=alt.Y('Annual GDP growth %:Q'),
        )
    )
    bar_colored = (
        alt.Chart(gdp_growth)
        .mark_bar()
        .encode(
            x='year',
            y=alt.Y('Annual GDP growth %:Q'),
            color=alt.value("orange")
        )
        .transform_filter(
            (alt.datum.year >= focus_start) & (alt.datum.year <= focus_end)
        )
    )

    return alt.hconcat(
        lines + lines_colored,
        bar + bar_colored
    )
