import pandas as pd

df_worldbank_gdp = pd.read_csv('data/worldbank_GDP_per_capita/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_4019678.csv',
                               quotechar='"')
df_worldbank_gdp.dropna(axis=1, how='all', inplace=True)
df_worldbank_gdp.drop(['Indicator Code'], axis=1, inplace=True)

pass
