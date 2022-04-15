# %%
import streamlit as st
import numpy as np
import re
from cache import dfc_imf_dot


@st.experimental_memo
def get_countries():
    'Get country list'
    return np.sort(dfc_imf_dot['Country Name'].unique())


@st.experimental_memo
def get_counterpart_countries(country):
    'Get counterpart country list based on country'
    counterpart_countries = (
        dfc_imf_dot
        .query(f"`Country Name` == '{country}'")['Counterpart Country Name']
        .unique())
    return ['All'] + list(np.sort(counterpart_countries))


@st.experimental_memo
def get_years(country, counterpart_country):
    'Get non nan years'
    years = [x for x in dfc_imf_dot.columns if bool(re.match(r'^\d{4}$', x))]
    if counterpart_country == 'All':
        return int(min(years)), int(max(years))
    non_nan_years = (
        dfc_imf_dot
        .query(f"`Country Name` == '{country}'")
        .query(f"`Counterpart Country Name` == '{counterpart_country}'")
        .loc[:, years]
        .dropna(axis=1, how='all')
        .columns
    )
    min_year = int(non_nan_years.min())
    max_year = int(non_nan_years.max())
    return min_year, max_year


# %%
def render_home():
    # %%
    # columns
    non_year_cols = ['Country Name', 'Counterpart Country Name',
                     'Indicator Name']
    # filter UI
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        country_list = get_countries()
        country = st.selectbox('Country', country_list)
    with col2:
        counterpart_country_list = get_counterpart_countries(country)
        counterpart_country = st.selectbox(
            'Counterpart Country', counterpart_country_list)
    with col3:
        min_year, max_year = get_years(country, counterpart_country)
        year = st.slider('Year', min_value=min_year, max_value=max_year)
    # df for debugging
    st.write('# Debug\n---')
    df = dfc_imf_dot.query(f"`Country Name` == '{country}'")
    if counterpart_country != 'All':
        st.write(counterpart_country)
        df = df.query(f"`Counterpart Country Name` == '{counterpart_country}'")
    df = df[non_year_cols + [str(year)]]
    df = df.sort_values(non_year_cols, ascending=True)
    st.dataframe(df)
