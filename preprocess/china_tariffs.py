# data from https://hts.usitc.gov/view/list

# %%

import tabula
import pandas as pd

csv_path = 'data/df_china_tariffs.csv'

try:
    df_china_tariffs = pd.read_csv(csv_path)
except FileNotFoundError:
    dfs = tabula.io.read_pdf('data/China Tariffs.pdf', pages='all')
    df_china_tariffs = pd.concat(dfs)
    df_china_tariffs = df_china_tariffs.rename(
        columns={'Harmonized Tariff Schedule 8-digit Subheading': 'china_tariffs'})
    df_china_tariffs = df_china_tariffs[['china_tariffs']]
    df_china_tariffs = df_china_tariffs.dropna()
    df_china_tariffs['china_tariffs'] = df_china_tariffs['china_tariffs'].str.replace(
        '.', '', regex=False)
    df_china_tariffs['china_tariffs'] = df_china_tariffs['china_tariffs'].str[:-2]
    df_china_tariffs = df_china_tariffs.drop_duplicates()
    df_china_tariffs = df_china_tariffs.sort_values(by=['china_tariffs'])
    df_china_tariffs = df_china_tariffs.reset_index()
    df_china_tariffs = df_china_tariffs[['china_tariffs']]
    df_china_tariffs.to_csv(csv_path)

# %%
