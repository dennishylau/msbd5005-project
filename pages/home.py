# %%
import streamlit as st
import numpy as np
import re
import altair as alt
import plotly.express as px
from cache import dfc_imf_dot
from constants import IMF_ECON_GROUPS
from enum import Enum


class Economies(Enum):
    COUNTRY_ECONOMIC_GROUP = "Show Countries and Economic Groups"
    COUNTRY = "Only Show Countries"
    ECONOMIC_GROUP = "Only Show Economic Groups"

    @property
    def ui_str(self) -> str:
        mapping = {
            "Only Show Countries": "Country",
            "Only Show Economic Groups": "Economic Group",
            "Show Countries and Economic Groups": "Country / Economic Group",
        }
        return mapping[self.value]


def get_countries(economies: Economies) -> list[str]:
    "Show list of countries / economies by `Economies`"
    df = dfc_imf_dot["Country Name"].unique()
    sorted_list = np.sort(df).tolist()
    if economies is Economies.COUNTRY:
        return [x for x in sorted_list if x not in IMF_ECON_GROUPS]
    elif economies is Economies.ECONOMIC_GROUP:
        return [x for x in sorted_list if x in IMF_ECON_GROUPS]
    else:
        return sorted_list


def get_counterpart_countries(economies: Economies, country: str) -> list[str]:
    "Get counterpart country list based on country"
    df = dfc_imf_dot.query(f"`Country Name` == '{country}'")[
        "Counterpart Country Name"
    ].unique()
    sorted_list = np.sort(df).tolist()
    if economies is Economies.COUNTRY:
        sorted_list = [x for x in sorted_list if x not in IMF_ECON_GROUPS]
    if economies is Economies.ECONOMIC_GROUP:
        sorted_list = [x for x in sorted_list if x in IMF_ECON_GROUPS]
    return ["All"] + list(sorted_list)


def get_top_n_counterpart_countries(
    economies: Economies,
    country: str,
    top_n: int = 10,
    year: int = 2021,
    trade_type: str = "Export",
) -> list[str]:
    "Get the top n counterpart countries, ranked by trade volume"
    df = dfc_imf_dot[
        (dfc_imf_dot["Country Name"] == country)
        & (dfc_imf_dot["Indicator Name"] == trade_type)
    ]
    trade_volume = (
        df.groupby(["Counterpart Country Name"])[str(year)]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    top_n_counters = trade_volume["Counterpart Country Name"].tolist()

    if economies is Economies.COUNTRY:
        top_n_counters = [x for x in top_n_counters if x not in IMF_ECON_GROUPS]
    if economies is Economies.ECONOMIC_GROUP:
        top_n_counters = [x for x in top_n_counters if x in IMF_ECON_GROUPS]

    top_n_counters = top_n_counters[:top_n]

    return top_n_counters


@st.experimental_memo
def get_years(country, counterpart_country):
    "Get non nan years"
    years = [x for x in dfc_imf_dot.columns if bool(re.match(r"^\d{4}$", x))]
    if counterpart_country == "All":
        return int(min(years)), int(max(years))
    non_nan_years = (
        dfc_imf_dot.query(f"`Country Name` == '{country}'")
        .query(f"`Counterpart Country Name` == '{counterpart_country}'")
        .loc[:, years]
        .dropna(axis=1, how="all")
        .columns
    )
    min_year = int(non_nan_years.min())
    max_year = int(non_nan_years.max())
    return min_year, max_year


def render_import_export_time_series(economies, country, selected_years, trade_type):
    """
    Plot import export time series using altair
    """
    min_selected_year, max_selected_year = selected_years
    top_n_counters = get_top_n_counterpart_countries(
        economies, country, 5, max_selected_year, trade_type
    )

    df = dfc_imf_dot[
        (dfc_imf_dot["Country Name"] == country)
        & (dfc_imf_dot["Counterpart Country Name"].isin(top_n_counters))
    ]
    num_columns = [
        c
        for c in df.columns
        if c.isnumeric()
        and (int(c) >= min_selected_year)
        and (int(c) <= max_selected_year)
    ]

    df = df[(df["Indicator Name"] == trade_type)]
    df = df[num_columns + ["Counterpart Country Name"]].melt(
        id_vars=["Counterpart Country Name"], var_name="Year", value_name="Volume"
    )

    line_chart = (
        alt.Chart(df, title="Trade volumns over time")
        .mark_line()
        .encode(
            x="Year",
            y="Volume",
            color="Counterpart Country Name",
            strokeDash="Counterpart Country Name",
        )
        .interactive()
    )
    st.altair_chart(line_chart, use_container_width=True)


def render_trade_partner_pie_chart(
    economies: Economies,
    country: str,
    selected_year: int,
    trade_type: str,
    top_n: int = 10,
):
    selected_year = str(selected_year)
    other_countries = dfc_imf_dot["Counterpart Country Name"].tolist()
    if economies is Economies.COUNTRY:
        other_countries = [x for x in other_countries if x not in IMF_ECON_GROUPS]
    if economies is Economies.ECONOMIC_GROUP:
        other_countries = [x for x in other_countries if x in IMF_ECON_GROUPS]

    df = dfc_imf_dot[
        (dfc_imf_dot["Country Name"] == country)
        & (dfc_imf_dot["Indicator Name"] == trade_type)
        & (dfc_imf_dot["Counterpart Country Name"].isin(other_countries))
    ][["Counterpart Country Name", selected_year]]

    trade_percentage = df[selected_year].fillna(0)
    df[selected_year] = trade_percentage / trade_percentage.sum()

    df = df.sort_values(selected_year, ascending=False)

    others = df.iloc[top_n:]
    df = df.iloc[:top_n]
    df.loc[len(df)] = ["Others", others[selected_year].sum()]

    pie_chart = px.pie(df, values=selected_year, names="Counterpart Country Name")

    st.plotly_chart(pie_chart, use_container_width=True)


def render_home():
    # %%
    # columns
    non_year_cols = ["Country Name", "Counterpart Country Name", "Indicator Name"]
    # filter UI
    col0, col1, col2, col3 = st.columns([1, 1, 1, 3])
    with col0:
        economies_opt_str = st.selectbox(
            "Economies", [x.value for x in Economies], index=1
        )
        economies = Economies(economies_opt_str)
    with col1:
        country_list = get_countries(economies)
        country = st.selectbox(economies.ui_str, country_list)
    with col2:
        counterpart_country_list = get_counterpart_countries(economies, country)
        counterpart_country = st.selectbox(
            f"Counterpart {economies.ui_str}", counterpart_country_list
        )
    with col3:
        min_year, max_year = get_years(country, counterpart_country)
        min_selected_year, max_selected_year = st.slider(
            "Year",
            min_value=min_year,
            max_value=max_year,
            value=(
                int(min_year + (max_year - min_year) * 0.25),
                int(min_year + (max_year - min_year) * 0.75),
            ),
        )

    # render import/export time series
    trade_type = st.selectbox("Trade type", ["Export", "Import"])
    render_import_export_time_series(
        economies, country, (min_selected_year, max_selected_year), trade_type
    )
    render_trade_partner_pie_chart(
        economies,
        country,
        max_selected_year,
        trade_type,
    )

    # st.line_chart(df)…
    # df = dfc_imf_dot.query(f"`Country Name` == '{country}'")
    # if counterpart_country != 'All':
    #     st.write(counterpart_country)
    #     df = df.query(f"`Counterpart Country Name` == '{counterpart_country}'")
    # df = df[non_year_cols + [str(year)]]
    # df = df.sort_values(non_year_cols, ascending=True)
    # st.dataframe(df)
