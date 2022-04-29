import pandas as pd
import streamlit as st
from preprocess import (
    df_wb_code,
    df_wb_trade,
    df_imf_dot,
    df_worldbank_gdp,
    df_population_15_64_percent,
    df_china_data,
    df_china_pyramid,
    df_china_pop)

COUNTRY_CODE_MAPPING = df_wb_code.set_index('code')['name'].to_dict()



@st.experimental_memo
def __cache(obj):
    return obj


def get_valid_countries(df) -> list[str]:
    """
    Returns valid countries base on the DataFrame preprocessed for map.

    A country is valid based on:
    1. has ISO3 code
    2. has latitude and longitude data from Google
    :param df: pd.DataFrame. Cached DataFrame preprocessed for trade balance map.
    :return valid_countries: list[str]. List of valid countries names in str.
    """
    valid_countries = df['Country Name'].unique().tolist()
    return valid_countries


def align_country_name(df: pd.DataFrame, country_name_col: str, code_col: str):
    df[country_name_col] = df[code_col].map(COUNTRY_CODE_MAPPING)
    df.dropna(subset=[country_name_col], inplace=True)
    return df


df_imf_dot = align_country_name(df_imf_dot, 'Country Name', 'Country Code ISO3')
df_imf_dot = align_country_name(df_imf_dot, 'Counterpart Country Name', 'Counterpart Country Code ISO3')
df_worldbank_gdp = align_country_name(df_worldbank_gdp, 'Country Name', 'Country Code')
df_population_15_64_percent = align_country_name(df_population_15_64_percent, 'Country Name', 'Country Code')

valid_countries = get_valid_countries(df_imf_dot)

# cache
dfc_wb_code = __cache(df_wb_code)
dfc_wb_trade = __cache(df_wb_trade)
dfc_imf_dot = __cache(df_imf_dot[(df_imf_dot['Country Name'].isin(valid_countries))
                                 & (df_imf_dot['Counterpart Country Name'].isin(valid_countries))])
dfc_china_data = __cache(df_china_data)
dfc_worldbank_gdp = __cache(df_worldbank_gdp)
dfc_population_15_64_percent = __cache(df_population_15_64_percent)
dfc_china_pyramid = __cache(df_china_pyramid)
dfc_china_pop = __cache(df_china_pop)
