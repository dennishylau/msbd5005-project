import streamlit as st
import plotly.express as px

from figure.map import update_data, plot_trade_balance_map


def render_2001_2010(dfc_china_data, dfc_imf_dot):
    MIN_YEAR = 1991
    MAX_YEAR = 2015

    df = dfc_china_data.reset_index().rename(columns={'index': 'Year'})
    df = df[(df['Year'] > MIN_YEAR) & (df['Year'] < MAX_YEAR)]
    fig1 = px.line(df, x='Year', y=['Trade Balance (Billions of US $)'],
                   title=f'Trade Balance (US $) of China from {MIN_YEAR} to {MAX_YEAR}')

    fig2 = px.line(df, x='Year', y=['GDP Growth (%)'],
                   title=f'GDP Growth (%) of China from {MIN_YEAR} to {MAX_YEAR}')
    fig2.layout.yaxis.tickformat = ',.2%'

    figs = [fig1, fig2]

    for fig in figs:
        fig.update_layout(
            showlegend=False,
            template='plotly_dark',
            autosize=True,
            height=200,
            margin=dict(
                l=60,
                r=0,
                b=30,
                t=30,
                pad=0,
                autoexpand=False))
        fig.add_vline(x=2001, line_dash="dot",
                      annotation_text="Joined WTO", annotation_position='top left')
        fig.add_vline(x=2002, line_dash="dot", annotation_position='top right',
                      annotation_text='ASEAN–China Free Trade Area (ACFTA) established')
        fig.add_vline(x=2008, line_dash="dot", annotation_position='top right',
                      annotation_text='Beijing Olympics 2008 Commenced')
        fig.add_vrect(x0=2007, x1=2008, line_width=0, fillcolor='red', opacity=0.25,
                      annotation_position='bottom right', annotation_text='Global Financial Crisis',
                      annotation_font={'color': '#ff3b3b', 'size': 15})

    _, _, desc_col, _, _ = st.columns([1, 1, 6, 1, 1])
    with desc_col:
        st.header("2001 - 2010")
        st.write('''
        If we look at the Trade Balance of China, we can see that China has not been opened to trades in the 90s.
        However, China became a member of the World Trade Organization (WTO) on 11 December 2001. China's accession
        to the WTO in 2001 causes the rise of Chinese exports to the US and Europe, this is known as the [China trade
        shock](https://en.wikipedia.org/wiki/China_shock) (Link to Wikipedia).

        Then in less than a year, China signed the ASEAN - China Free Trade Area (ACFTA) framework agreement on 4
        November 2002 with the ten member states of the Association of Southeast Asian Nations (ASEAN). This framework
        eliminates tariffs of the products from the signatories by 90%.

        Since China began to open to trade, China's trade balance and GDP growth began to steadily increase until 2008.
        On 8 August 2008, the Beijing Olympics commenced. China's trade balance reached the peak. However, the impact of
        the Global Financial Crisis that took place between 2007 and 2008 had a huge effect on China's GDP Growth.
        ''')
        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

    _, _, desc_col, _, _ = st.columns([1, 1, 6, 1, 1])
    with desc_col:
        st.header("WTO & ACFTA impacts")
        st.write('''       
        On the right, we have a map showing China's top 10 best trade partners and worst 10 trade partners 
        in terms of trade balance. You can slide through the slide bar from 2002 to 2010. Green indicates profit and
        red indicates loss. The width of each line indicates the volume.

        As you are sliding through, you should see that China's mainly gained profit from the US and European countries.
        This is due to the fact that China joined WTO in 2001.
        However, what contradicts to our intuition is that China has been losing money to most countries that signed the 
        ACFTA framework.
        ''')

        chosen_country = 'China'
        min_year = 2002
        max_year = 2010
        chosen_year = st.slider('Year', min_year, max_year, 2002)

        data = update_data(dfc_imf_dot, chosen_country,
                           chosen_year, chosen_top_n=10, chosen_bottom_n=10)
        trade_balance_map = plot_trade_balance_map(data, chosen_country, chosen_year, chosen_top_n=10,
                                                   chosen_bottom_n=10)
        st.plotly_chart(trade_balance_map, use_container_width=True)
