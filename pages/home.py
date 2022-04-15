# %%
import streamlit as st
import numpy as np
import re
from cache import dfc_imf_dot
from constants import IMF_ECON_GROUPS
from enum import Enum


class Economies(Enum):
    COUNTRY_ECONOMIC_GROUP = 'Show Countries and Economic Groups'
    COUNTRY = 'Only Show Countries'
    ECONOMIC_GROUP = 'Only Show Economic Groups'

    @property
    def ui_str(self) -> str:
        mapping = {
            'Only Show Countries': 'Country',
            'Only Show Economic Groups': 'Economic Group',
            'Show Countries and Economic Groups': 'Country / Economic Group'
        }
        return mapping[self.value]


def get_countries(economies: Economies) -> list[str]:
    'Show list of countries / economies by `Economies`'
    df = dfc_imf_dot['Country Name'].unique()
    sorted_list = np.sort(df).tolist()
    if economies is Economies.COUNTRY:
        return [x for x in sorted_list if x not in IMF_ECON_GROUPS]
    elif economies is Economies.ECONOMIC_GROUP:
        return [x for x in sorted_list if x in IMF_ECON_GROUPS]
    else:
        return sorted_list


def get_counterpart_countries(economies: Economies, country: str) -> list[str]:
    'Get counterpart country list based on country'
    df = (
        dfc_imf_dot
        .query(f"`Country Name` == '{country}'")['Counterpart Country Name']
        .unique())
    sorted_list = np.sort(df).tolist()
    if economies is Economies.COUNTRY:
        sorted_list = [x for x in sorted_list if x not in IMF_ECON_GROUPS]
    if economies is Economies.ECONOMIC_GROUP:
        sorted_list = [x for x in sorted_list if x in IMF_ECON_GROUPS]
    return ['All'] + list(sorted_list)


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


def render_home():
    # %%
    # columns
    non_year_cols = ['Country Name', 'Counterpart Country Name',
                     'Indicator Name']
    # filter UI
    col0, col1, col2, col3 = st.columns([1, 1, 1, 3])
    with col0:
        economies_opt_str = st.selectbox(
            'Economies', [x.value for x in Economies])
        economies = Economies(economies_opt_str)
    with col1:
        country_list = get_countries(economies)
        country = st.selectbox(
            economies.ui_str,
            country_list)
    with col2:
        counterpart_country_list = get_counterpart_countries(
            economies, country)
        counterpart_country = st.selectbox(
            f'Counterpart {economies.ui_str}',
            counterpart_country_list)
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
