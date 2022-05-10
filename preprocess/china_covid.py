import streamlit as st
import pandas as pd
import numpy as np


BIN_CUTS = np.array([0, 10, 50, 100, 500, 1000, 5000, 10000])
BIN_IDX = list(range(len(BIN_CUTS) - 1))


def get_df_total_death():
    df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
    df = df[df['Country/Region'] == 'China']
    df_total_death = df.iloc[:, [-1]]
    df_total_death.name = 'total_death'
    df_total_death = df.iloc[:, [0]].join(df_total_death)
    df_total_death.columns = ['Province/State', 'total_death']

    zero_mask = df_total_death['total_death'] == 0
    s_total_death_log = np.log10(
        df_total_death['total_death'],
        where=np.logical_not(zero_mask))
    s_total_death_log[zero_mask] = 0
    df_total_death['total_death_log'] = s_total_death_log
    df_total_death['total_death_binned'] = pd.cut(
        df_total_death['total_death'],
        BIN_CUTS,
        labels=BIN_IDX,
        include_lowest=True, right=False)
    return df_total_death.sort_index()


@st.experimental_memo
def get_df_death_ts_gp(location):
    # set default location for simplicity
    location = location if location else 'Hubei'
    df = pd.read_csv('data/time_series_covid19_deaths_global.csv')
    df = df[df['Country/Region'] == 'China']
    df_country = df.iloc[:, 4:].sum().T
    df_city = df.query(f'`Province/State` == "{location}"').iloc[:, 4:].T
    df_death_ts = pd.concat([df_city, df_country])
    df_death_ts = df_death_ts.diff()
    df_death_ts['Date'] = pd.to_datetime(df_death_ts.index)
    df_death_ts['Date'] = df_death_ts['Date'].dt.to_period('M')
    df_death_ts_gp = df_death_ts.groupby('Date').sum()
    df_death_ts_gp.set_index(
        df_death_ts_gp.index.to_timestamp(how='start'),
        inplace=True)
    df_death_ts_gp.columns = ['Region Deaths', 'Country Deaths']
    df_death_ts_gp['Date'] = df_death_ts_gp.index
    return df_death_ts_gp


df_total_death = get_df_total_death()
