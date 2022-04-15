# %%
import streamlit as st


# %%
# page setup
st.set_page_config(layout="wide")

# load data and cache them
# only init cache after calling set_page_config()
if True:
    from cache import dfc_wb_code, dfc_wb_trade, dfc_imf_dot


# %% Sidebar

with st.sidebar:
    '# Filters'

    economies = st.multiselect(
        'Economies', dfc_wb_code.name.sort_values(),
        key='economies')
    if len(economies) == 0:
        economies = ['World']

    year_start, year_end = st.slider(
        'Select year',
        1960, 2020, (1960, 2020)
    )

# %% Body

"""
# MSBD5005 Project
"""

left_column, right_column = st.columns(2)

with left_column:
    '## Trade (% GDP)'
    st.line_chart(dfc_wb_trade[economies].loc[year_start: year_end])
with right_column:
    st.dataframe(dfc_imf_dot)

# %% Reference
'''
## Reference
- World Bank Trade (% of GDP): https://data.worldbank.org/indicator/NE.TRD.GNFS.ZS
- WBGAPI for downloading WorldBank data: https://nbviewer.org/github/tgherzog/wbgapi/blob/master/examples/wbgapi-cookbook.ipynb
- Internation Monetary Fund Direction of Trade Statistics: https://data.imf.org/?sk=9d6028d4-f14a-464c-a2f2-59b2cd424b85&sId=1409151240976
'''
