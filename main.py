# %%
import streamlit as st
import pandas as pd
# import wbgapi as wb

# %% page setup

st.set_page_config(layout="wide")


# %% World Bank Country Code
df_country = pd.read_csv('data/country.csv')
# %%
df_country.columns = ['group', 'group_name', 'code', 'name']
# code to name mappings
df_group_code = df_country[['group', 'group_name']].drop_duplicates()
df_group_code.columns = ['code', 'name']
df_country_code = df_country[['code', 'name']].drop_duplicates()
df_all_code = pd.concat([df_country_code, df_group_code])
# read country group
df_country_group = df_country[['code', 'name', 'group']].groupby(
    ['code', 'name']).agg(list)
df_country_group.reset_index(inplace=True)
# %% World Bank Trade (% of GDP) Data

# Download
# df = wb.data.DataFrame('NE.TRD.GNFS.ZS')

# remove economies with unknown name mapping
df_trade = pd.read_csv('data/NE.TRD.GNFS.ZS.csv')
df_trade = df_trade.merge(
    df_all_code, how='left',
    left_on='economy', right_on='code')
df_trade = df_trade[df_trade.name.notnull()]
df_trade = df_trade.drop(['economy', 'code'], axis=1)
df_trade.columns = df_trade.columns.str.replace('YR', '')
# rename_axis must be called after .T for st.line_chart to work
df_trade = df_trade.set_index('name').T.rename_axis(None, axis=1)
df_trade = df_trade.rename_axis('year', axis=0)
df_trade.index = df_trade.index.astype(int)

# %% Sidebar

with st.sidebar:
    '# Filters'

    economies = st.multiselect(
        'Economies', df_all_code.name.sort_values(),
        key='economies')
    if len(economies) == 0:
        economies = ['World']

    year_start, year_end = st.slider(
        'Select year',
        1960, 2020, (1960, 2020)
    )

# %% Body

"""
# MSBD5005 Project
"""

left_column, right_column = st.columns(2)

with left_column:
    '## Trade (% GDP)'
    st.line_chart(df_trade[economies].loc[year_start: year_end])


# %% Reference
'''
## Reference
- World Bank Trade (% of GDP): https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS
- WBGAPI for downloading WorldBank data: https://nbviewer.org/github/tgherzog/wbgapi/blob/master/examples/wbgapi-cookbook.ipynb
'''
