import pandas as pd
import textwrap
from .china_tariffs import df_china_tariffs

df_comtrade = pd.read_csv('data/comtrade_ch_us_ex.csv')
df_comtrade = df_comtrade[df_comtrade['Commodity Code'] != 'TOTAL']
df_comtrade_agg_2 = df_comtrade.query('`Aggregate Level` == 2')[
    ['Commodity Code', 'Commodity']].drop_duplicates()
df_comtrade_agg_4 = df_comtrade.query('`Aggregate Level` == 4')[
    ['Commodity Code', 'Commodity']].drop_duplicates()
df_comtrade_agg_6 = df_comtrade.query('`Aggregate Level` == 6')[
    ['Trade Flow', 'Commodity Code', 'Commodity', 'Trade Value (US$)']].drop_duplicates()
df_comtrade_agg_6['agg_4'] = df_comtrade_agg_6['Commodity Code'].str[:4]
df_comtrade_agg_6['agg_2'] = df_comtrade_agg_6['Commodity Code'].str[:2]
df_comtrade = df_comtrade_agg_6.merge(
    df_comtrade_agg_4, how='left', left_on='agg_4', right_on='Commodity Code',
    suffixes=('_agg_6', '_agg_4')).merge(
    df_comtrade_agg_2, how='left', left_on='agg_2', right_on='Commodity Code',
    suffixes=('', '_agg_2'))
df_comtrade = df_comtrade.query('`Trade Flow` == "Export"')
df_china_tariffs['tariff'] = 'true'
df_comtrade['Commodity Code_agg_6'] = df_comtrade['Commodity Code_agg_6'].astype(
    str)
df_china_tariffs['china_tariffs'] = df_china_tariffs['china_tariffs'].astype(
    str)
df_comtrade = df_comtrade.merge(
    df_china_tariffs, how='left', left_on='Commodity Code_agg_6',
    right_on='china_tariffs')
df_comtrade['tariff'] = df_comtrade['tariff'].fillna('false')

# short for display within treemap
df_comtrade['Commodity_short'] = df_comtrade['Commodity'].apply(
    lambda x: '<br>'.join(
        textwrap.wrap(x, width=80, max_lines=2, placeholder='...')))
df_comtrade['Commodity_agg_4_short'] = df_comtrade['Commodity_agg_4'].apply(
    lambda x: '<br>'.join(
        textwrap.wrap(x, width=50, max_lines=2, placeholder='...')))
df_comtrade['Commodity_agg_6_short'] = df_comtrade['Commodity_agg_6'].apply(
    lambda x: '<br>'.join(
        textwrap.wrap(x, width=25, placeholder='...')))

# long for display within label
for x in ['Commodity', 'Commodity_agg_4', 'Commodity_agg_6']:
    df_comtrade[f'{x}_long'] = df_comtrade[x].apply(
        lambda x: '<br>'.join(
            textwrap.wrap(x, width=80, placeholder='...')))
