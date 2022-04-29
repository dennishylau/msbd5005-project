import pandas as pd
import plotly.express as px


def prepare_data_by_trade_type(dfc_imf_dot, country, selected_year, trade_type, top_n=10):
    selected_year = str(selected_year)
    other_countries = dfc_imf_dot['Counterpart Country Name'].tolist()

    df = dfc_imf_dot[(dfc_imf_dot['Country Name'] == country)
                     & (dfc_imf_dot['Indicator Name'] == trade_type)
                     & (dfc_imf_dot['Counterpart Country Name'].isin(other_countries))][
        ['Counterpart Country Name', selected_year]]

    trade_percentage = df[selected_year].fillna(0)
    df[selected_year] = trade_percentage / trade_percentage.sum()

    df = df.sort_values(selected_year, ascending=False)

    others = df.iloc[top_n:]
    df = df.iloc[:top_n]
    df.loc[len(df)] = ['Others', others[selected_year].sum()]
    return df


def prepare_data(dfc_imf_dot, country, selected_year, top_n=10):
    import_df = prepare_data_by_trade_type(dfc_imf_dot, country, selected_year, 'Import', top_n)
    export_df = prepare_data_by_trade_type(dfc_imf_dot, country, selected_year, 'Export', top_n)

    import_df['Indicator Name'] = 'Import'
    export_df['Indicator Name'] = 'Export'

    return pd.concat([import_df, export_df], ignore_index=True)


def prepare_color_mapping(df):
    """Align both pie charts color."""
    unique_countries = df['Counterpart Country Name'].unique()
    colors = px.colors.qualitative.Alphabet
    return {country: color for country, color in zip(unique_countries, colors)}


def plot_trade_partner_pie_chart(df: pd.DataFrame, country: str, selected_year: int, trade_type: str,
                                 color_mapping: dict, top_n: int = 10):
    df = df[df['Indicator Name'] == trade_type]
    pie_chart = px.pie(df, values=str(selected_year), names='Counterpart Country Name',
                       title=f'{trade_type}s of {country} in {selected_year}', color='Counterpart Country Name',
                       color_discrete_map=color_mapping)
    return pie_chart
