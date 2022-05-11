# %%
import streamlit as st
from utils import margin
from figure.history_2011_bt import get_fig_bt
from figure.history_2011_dot import get_fig_dot
from figure.history_2011_comtrade import write_fig_goods

# %%
DESCRIBE_TRADE_WAR = '''
    # 2018 China-US Trade War
    Since China's entry into the World Trade Organization, China's export to the United States has grown steadily and substantially, and reached a historic high at the time in 2017.

    In 2018, US President Donald Trump began setting tariffs on Chinese imports in an attempt to reduce trade deficit, and to curb alleged intellectual property piracy.
    '''


DESCRIBE_DIRECTION_OF_TRADE = '''
    The graph to the left shows the historic data of China's export and import against the United States, provided by the International Monetary Fund. From the mid-1990s, China has steadily widen its trade surplus against the United States. Note that the amount is in nominal USD, unadjusted for inflation.

    A widening trade surplus for China means a widening trade deficit for the United States, which President Donald Trump claimed will be unfavorable to the US economy.

    The Trade War had immediate effect on China's net export to the United States, which in 2019 fell by 30 billion USD year-over-year. In the short run, President Donald Trump's effort seemed to have paid off.
    '''


DESCRIBE_TREEMAP = '''
    The following treemap shows all categories and subcategories of commodities impacted by the Trade War.

    You can click a category to zoom in, and see its corresponding subcategories in more detail. Size of boxes within the treemap are proportional to the trade value for the commodity category.

    Red boxes indicate categories with additional tariff specific to China; grey boxes indicate unimpacted categories; while navy boxes have some subcategories that were impacted, and others that were not impacted. Click on navy boxes to explore subcategories impacts.
    '''

DESCRIBE_BALANCE_OF_TRADE = '''
    However, when we look at the balance of trade data of China provided by the World Bank, the United States's attempt to reduce trade deficit did not devastate China's foreign trade. In fact, after a slump in trade balance in 2018, China has started recovering in 2019. China's GDP growth maintained a respectable 6.75% in 2019 despite the Trade War.

    In 2020, 2 years after the onset of the Trade War, China's trade balance reached historic high, while the trade balance in terms of percentage GDP remained stable. GDP Growth, however, has taken a hit from COVID-19, and was largely unrelated the remaining impact of the Trade War.
    '''


def render_2011_2020():
    st.write(DESCRIBE_TRADE_WAR)

    st.write('---')

    col11, col12 = st.columns([2, 1])
    with col11:
        st.plotly_chart(get_fig_dot(), use_container_width=True)
    with col12:
        margin(7)
        st.write(DESCRIBE_DIRECTION_OF_TRADE)

    st.write('---')

    st.write(DESCRIBE_TREEMAP)
    write_fig_goods()

    st.write('---')

    col21, col22 = st.columns([1, 2])
    with col21:
        margin(7)
        st.write(DESCRIBE_BALANCE_OF_TRADE)
    with col22:
        st.plotly_chart(get_fig_bt(), use_container_width=True)
