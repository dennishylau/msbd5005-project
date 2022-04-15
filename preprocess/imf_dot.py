# %%
import pandas as pd
import re


def preprecess_imf_dot():

    # download this file separately, too large for git
    df_imf_dot_raw = pd.read_csv(
        './data/DOT_03-28-2022 04-15-57-36_timeSeries.csv')

    years = [x for x in df_imf_dot_raw.columns
             if bool(re.match(r'^\d{4}$', x))]

    df_imf_dot = (
        df_imf_dot_raw
        .query("Attribute == 'Value'")
        .query(
            """`Indicator Name` in [
                'Goods, Value of Exports, Free on board (FOB), US Dollars',
                'Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars',
                'Goods, Value of Trade Balance, US Dollars'
            ]""".replace('\n', ''))
        .loc[:, ['Country Name', 'Counterpart Country Name', 'Indicator Name'] + years]
        .dropna(how='all', subset=years)
        .sort_values(['Country Name', 'Counterpart Country Name', 'Indicator Name'], ascending=True))
    df_imf_dot['Indicator Name'].replace({
        'Goods, Value of Exports, Free on board (FOB), US Dollars': 'Export',
        'Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars': 'Import',
        'Goods, Value of Trade Balance, US Dollars': 'Trade Balance'
    }, inplace=True)
    for y in years:
        df_imf_dot[y] = df_imf_dot[y].astype(float)
    return df_imf_dot

# %%


try:
    df_imf_dot = pd.read_parquet('./data/imf_dot.parq')
except FileNotFoundError:
    df_imf_dot = preprecess_imf_dot()
    df_imf_dot.to_parquet('./data/imf_dot.parq')
