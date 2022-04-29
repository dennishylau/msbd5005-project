import pandas as pd


def china_population_growth(df_china_pyramid):
    df_population = df_china_pyramid.groupby("year")['people'].sum()
    return df_population


df_china_data = pd.read_parquet('data/macrotrends_china_data.snappy.parquet')
df_china_pyramid = pd.read_csv('data/china_pyramid.csv')
df_china_pop = china_population_growth(df_china_pyramid)
