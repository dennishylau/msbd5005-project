import altair as alt
import pandas as pd


def get_pyramid(dfc_china_pyramid, min_year, max_year, step=1):
    slider = alt.binding_range(min=min_year, max=max_year, step=step)
    select_year = alt.selection_single(name='Year', fields=['year'],
                                       bind=slider, init={'year': min_year})

    dfc_china_pyramid['people'] = dfc_china_pyramid.groupby(
        ['year', 'sex'])['people'].apply(lambda x: x / x.sum())

    base = alt.Chart(dfc_china_pyramid).add_selection(
        select_year
    ).transform_filter(
        select_year
    ).properties(
        width=230
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
    ).mark_text(color='white').properties(title='Age', width=35)

    right = base.transform_filter(
        alt.datum.sex == 'M'
    ).encode(
        y=alt.Y('Age:O', axis=None, sort=alt.SortOrder('descending')),
        x=alt.X('sum(people):Q', title='population'),
        color=alt.Color('sex:N', scale=color_scale, legend=None)
    ).mark_bar().properties(title='Male')

    left_rule = alt.Chart(
        pd.DataFrame({"Age": [20, 65]})
    ).mark_rule(
        clip=False,
        color='white'
    ).encode(
        y=alt.Y('Age:O', axis=None, sort=alt.SortOrder('descending')),
        size=alt.SizeValue(1)
    )

    right_rule = alt.Chart(
        pd.DataFrame({"Age": [20, 65]})
    ).mark_rule(
        clip=False,
        color='white'
    ).encode(
        y=alt.Y('Age:O', axis=None, sort=alt.SortOrder('descending')),
        size=alt.SizeValue(1)
    )

    right_ind = alt.Chart(
        pd.DataFrame({
            "x": [.15]*3,
            "Age": [5, 25, 70],
            "Group": ["Dependents", "Tax payers", "Retirees"]
        })
    ).encode(
        x='x:Q',
        y=alt.Y('Age:N', axis=None, sort=alt.SortOrder('descending')),
        text=alt.Text('Group:N'),
    ).mark_text(
        color='white',
        # clip=False
    ).properties(title='Group', width=35)

    left = (left + left_rule).resolve_scale()
    right = (right + right_rule).resolve_scale() + right_ind

    return alt.concat(left, middle, right, spacing=5)
