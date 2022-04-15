import pandas as pd
from .wb_country import df_wb_code
# %% World Bank Trade (% of GDP) Data

# Download
# df = wb.data.DataFrame('NE.TRD.GNFS.ZS')

# remove economies with unknown name mapping
df_wb_trade = pd.read_csv('data/NE.TRD.GNFS.ZS.csv')
df_wb_trade = df_wb_trade.merge(
    df_wb_code, how='left',
    left_on='economy', right_on='code')
df_wb_trade = df_wb_trade[df_wb_trade.name.notnull()]
df_wb_trade = df_wb_trade.drop(['economy', 'code'], axis=1)
df_wb_trade.columns = df_wb_trade.columns.str.replace('YR', '')
# rename_axis must be called after .T for st.line_chart to work
df_wb_trade = df_wb_trade.set_index('name').T.rename_axis(None, axis=1)
df_wb_trade = df_wb_trade.rename_axis('year', axis=0)
df_wb_trade.index = df_wb_trade.index.astype(int)
