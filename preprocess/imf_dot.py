import pandas as pd
import re


def preprecess_imf_dot():

    # both CSVs can be downloaded from IMF website
    meta_df = pd.read_csv('./data/Metadata_DOT_03-28-2022 04-15-57-36_timeSeries.csv')
    # takes row 11:1835 which is exactly the definition of country code
    meta_df = meta_df.iloc[11:1835][['Metadata Attribute', 'Metadata Value']]
    country_code = meta_df[meta_df['Metadata Attribute'] == 'Country Code']['Metadata Value'].to_numpy()
    country_iso3_code = meta_df[meta_df['Metadata Attribute'] == 'Country ISO 3 Code']['Metadata Value'].to_numpy()

    country_code_map = {int(code): iso3_code for code, iso3_code in zip(country_code, country_iso3_code)}

    df_imf_dot_raw = pd.read_csv('./data/DOT_03-28-2022 04-15-57-36_timeSeries.csv', low_memory=False)

    years = [x for x in df_imf_dot_raw.columns if bool(re.match(r'^\d{4}$', x))]

    df_imf_dot_raw['Indicator Name'].replace({
        'Goods, Value of Exports, Free on board (FOB), US Dollars': 'Export',
        'Goods, Value of Imports, Cost, Insurance, Freight (CIF), US Dollars': 'Import',
        'Goods, Value of Trade Balance, US Dollars': 'Trade Balance'}, inplace=True)

    indicator_filter = ['Export', 'Import', 'Trade Balance']

    df_imf_dot_raw['Country Code ISO3'] = df_imf_dot_raw['Country Code'].map(country_code_map)
    df_imf_dot_raw['Counterpart Country Code ISO3'] = df_imf_dot_raw['Counterpart Country Code'].map(country_code_map)

    df_imf_dot = (df_imf_dot_raw[(df_imf_dot_raw['Attribute'] == 'Value')
                                 & (df_imf_dot_raw['Indicator Name'].isin(indicator_filter))]
                  .loc[:, ['Country Name', 'Counterpart Country Name', 'Indicator Name',
                           'Country Code ISO3', 'Counterpart Country Code ISO3'] + years]
                  .dropna(how='all', subset=years)
                  .sort_values(['Country Name', 'Counterpart Country Name', 'Indicator Name',
                                'Country Code ISO3', 'Counterpart Country Code ISO3'], ascending=True))

    for y in years:
        df_imf_dot[y] = df_imf_dot[y].astype(float)

    lat_lon_lookup = pd.read_csv('./data/country_ISO3_lat_lon_lookup.csv')
    lat_lon_lookup['ISO3 Code'] = lat_lon_lookup['Alpha-3 code'].str.replace('"', '').str.strip()
    latitude_lookup_dict = lat_lon_lookup.set_index('ISO3 Code')['Latitude (average)'].str.replace('"', '').astype(
        float).to_dict()
    longitude_lookup_dict = lat_lon_lookup.set_index('ISO3 Code')['Longitude (average)'].str.replace('"', '').astype(
        float).to_dict()

    df_imf_dot['latitude'] = df_imf_dot['Country Code ISO3'].map(latitude_lookup_dict)
    df_imf_dot['longitude'] = df_imf_dot['Country Code ISO3'].map(longitude_lookup_dict)

    df_imf_dot['Counterpart latitude'] = df_imf_dot['Counterpart Country Code ISO3'].map(latitude_lookup_dict)
    df_imf_dot['Counterpart longitude'] = df_imf_dot['Counterpart Country Code ISO3'].map(longitude_lookup_dict)

    return df_imf_dot


try:
    df_imf_dot = pd.read_parquet('./data/imf_dot.parq')
except FileNotFoundError:
    df_imf_dot = preprecess_imf_dot()
    df_imf_dot.to_parquet('./data/imf_dot.parq')
