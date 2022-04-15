import pandas as pd

# %% World Bank Country Code
df_wb_country = pd.read_csv('data/country.csv')
# %%
df_wb_country.columns = ['group', 'group_name', 'code', 'name']
# code to name mappings
df_wb_group_code = df_wb_country[['group', 'group_name']].drop_duplicates()
df_wb_group_code.columns = ['code', 'name']
df_wb_country_code = df_wb_country[['code', 'name']].drop_duplicates()
df_wb_code = pd.concat([df_wb_country_code, df_wb_group_code])
# read country group
df_wb_country_group = df_wb_country[['code', 'name', 'group']].groupby(
    ['code', 'name']).agg(list)
df_wb_country_group.reset_index(inplace=True)
