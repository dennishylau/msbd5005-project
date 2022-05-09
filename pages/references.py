import streamlit as st


def render_references():
    st.write('''
    ## Reference
    - Macrotrends: https://www.macrotrends.net/countries/CHN/china/gdp-gross-domestic-product
    - USITC Tariff Data: https://hts.usitc.gov/view/list
    - World Bank Trade (% of GDP): https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS
    - WBGAPI for downloading WorldBank data: https://nbviewer.org/github/tgherzog/wbgapi/blob/master/examples/wbgapi-cookbook.ipynb
    - Internation Monetary Fund Direction of Trade Statistics: https://data.imf.org/?sk=9d6028d4-f14a-464c-a2f2-59b2cd424b85&sId=1409151240976
    - China Province Boundary: https://www.kaggle.com/datasets/quanncore/china-province-geojson
    - China COVID Data: https://github.com/CSSEGISandData/COVID-19
    ''')
