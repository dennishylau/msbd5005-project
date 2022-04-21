import pandas as pd
import plotly.express as px


def plot_trade_partner_pie_chart(dfc_imf_dot: pd.DataFrame, country: str, selected_year: int, trade_type: str, top_n: int = 10):
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

    pie_chart = px.pie(df, values=selected_year, names='Counterpart Country Name')
    return pie_chart
