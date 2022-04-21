import streamlit as st
from preprocess import df_wb_code, df_wb_trade, df_imf_dot, df_imf_map


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


valid_countries = get_valid_countries(df_imf_map)

# cache
dfc_wb_code = __cache(df_wb_code)
dfc_wb_trade = __cache(df_wb_trade)
dfc_imf_dot = __cache(df_imf_dot[(df_imf_dot['Country Name'].isin(valid_countries))
                                 & (df_imf_dot['Counterpart Country Name'].isin(valid_countries))])
dfc_imf_map = __cache(df_imf_map)
