import pandas as pd

df_worldbank_gdp = pd.read_csv('data/worldbank_GDP/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_4019306.csv',
                               quotechar='"')
df_worldbank_gdp.dropna(axis=1, how='all', inplace=True)
df_worldbank_gdp.drop(['Indicator Code'], axis=1, inplace=True)

df_worldbank_gdp_per_cap = pd.read_csv('data/worldbank_GDP_per_capita/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_4019678.csv',
                                       quotechar='"')
df_worldbank_gdp_per_cap.dropna(axis=1, how='all', inplace=True)
df_worldbank_gdp_per_cap.drop(['Indicator Code'], axis=1, inplace=True)

df_population_15_64_percent = pd.read_csv(
    'data/worldbank_population_15-64/API_SP.POP.1564.TO.ZS_DS2_en_csv_v2_4022255.csv',
    quotechar='"')
df_population_15_64_percent.dropna(axis=1, how='all', inplace=True)
df_population_15_64_percent.drop(['Indicator Code'], axis=1, inplace=True)

df_china_gdp_comp = pd.read_csv(
    'data/worldbank_GDP_composition/china_gdp_comp.csv')
df_china_gdp_comp = df_china_gdp_comp.melt(
    'Indicator Name',
    [c for c in df_china_gdp_comp.columns if c.isnumeric()],
    'year',
    '% of GDP'
).rename({"Indicator Name": "Sector"}, axis=1)
df_china_gdp_comp['year'] = df_china_gdp_comp['year'].astype(int)
