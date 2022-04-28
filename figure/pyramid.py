import altair as alt
import pandas as pd


def get_pyramid(dfc_china_pyramid, min_year, max_year, step=1):
    slider = alt.binding_range(min=min_year, max=max_year, step=step)
    select_year = alt.selection_single(name='Year', fields=['year'],
                                       bind=slider, init={'year': min_year})

    base = alt.Chart(dfc_china_pyramid).add_selection(
        select_year
    ).transform_filter(
        select_year
    ).properties(
        width=350
    )

    color_scale = alt.Scale(domain=['M', 'F'],
                            range=['#1f77b4', '#e377c2'])

    left = base.transform_filter(
        alt.datum.sex == 'F'
    ).encode(
        y=alt.Y('Age:O', axis=None, sort=alt.SortOrder('descending')),
        x=alt.X('sum(people)',
                title='population',
                sort=alt.SortOrder('descending')),
        color=alt.Color('sex:N', scale=color_scale, legend=None)
    ).mark_bar().properties(title='Female')

    middle = base.encode(
        y=alt.Y('Age:N', axis=None, sort=alt.SortOrder('descending')),
        text=alt.Text('Age'),
    ).mark_text(color='white').properties(width=35)

    right = base.transform_filter(
        alt.datum.sex == 'M'
    ).encode(
        y=alt.Y('Age:O', axis=None, sort=alt.SortOrder('descending')),
        x=alt.X('sum(people):Q', title='population'),
        color=alt.Color('sex:N', scale=color_scale, legend=None)
    ).mark_bar().properties(title='Male')

    return alt.concat(left, middle, right, spacing=5)
