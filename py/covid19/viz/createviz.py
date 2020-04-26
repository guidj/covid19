import argparse
import os.path
from typing import Dict, Any

import altair as alt
import datetime
import pandas as pd

from covid19 import typedef
from covid19.data import preproc
from covid19.data import generate


def create_viz_growth_simulation(charts_path: str) -> None:
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2020, 1, 15)

    df_sim_a = generate.generate_infection_projection_data(
        start_date, end_date, starting_cases=5, growth_rate=2.5
    )
    df_sim_b = generate.generate_infection_projection_data(
        start_date, end_date, starting_cases=5, growth_rate=2.0
    )
    df_sim_c = generate.generate_infection_projection_data(
        start_date, end_date, starting_cases=5, growth_rate=1.5
    )

    viz_path = os.path.join(charts_path, "virality-simulation.html")

    agg_count_chart_a = (
        alt.Chart(df_sim_a)
        .mark_line(point=True, color="red")
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.CONFIRMED, title="# Cases"),
            color=alt.Color("%s:N" % typedef.Columns.GROWTH_RATE, title="Growth Rate"),
            tooltip="%s:N" % typedef.Columns.CONFIRMED,
        )
        .interactive()
        .properties(width=600, height=400)
    )

    agg_count_chart_b = (
        alt.Chart(df_sim_b)
        .mark_line(point=True, color="red")
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.CONFIRMED, title="# Cases"),
            color=alt.Color("%s:N" % typedef.Columns.GROWTH_RATE, title="Growth Rate"),
            tooltip="%s:N" % typedef.Columns.CONFIRMED,
        )
        .interactive()
        .properties(width=600, height=400)
    )

    agg_count_chart_c = (
        alt.Chart(df_sim_c)
        .mark_line(point=True, color="red")
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.CONFIRMED, title="# Cases"),
            color=alt.Color("%s:N" % typedef.Columns.GROWTH_RATE, title="Growth Rate"),
            tooltip="%s:N" % typedef.Columns.CONFIRMED,
        )
        .interactive()
        .properties(width=600, height=400)
    )

    agg_count_chart_a.configure(numberFormat="~s")
    agg_count_chart_a.configure_legend(
        strokeColor="gray",
        fillColor="#EEEEEE",
        padding=10,
        cornerRadius=10,
        orient="top-right",
    )

    final_chart = agg_count_chart_a + agg_count_chart_b + agg_count_chart_c
    final_chart.properties(title="Exponential Growth").save(
        viz_path, embed_options={"renderer": "svg"}
    )


def create_viz_world_confirmed_and_rate(
    charts_path: str, dfs: Dict[str, pd.DataFrame]
) -> None:
    df_world_agg_confirmed = dfs["world-agg-confirmed"]
    df_world_agg_growth_rate = dfs["world-agg-growth-rate"]

    viz_path = os.path.join(charts_path, "world-agg-chart.html")

    world_agg_confirmed_chart = (
        alt.Chart(df_world_agg_confirmed)
        .mark_line(point=True, color="red")
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.CONFIRMED, title="# Cases"),
            tooltip=typedef.Columns.CONFIRMED,
        )
        .properties(width=600, height=400)
    ).properties(title="Global # Confirmed Cases")

    world_agg_growth_rate_chart = (
        alt.Chart(df_world_agg_growth_rate)
        .mark_line(point=True, color="red")
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.GROWTH_RATE, title="Rate of New Cases"),
            tooltip="%s:N" % typedef.Columns.GROWTH_RATE,
        )
        .properties(width=600, height=120, title="Global Rate of New Cases")
    )

    world_agg_confirmed_chart.configure(numberFormat="~s")
    world_agg_confirmed_chart.configure_legend(
        strokeColor="gray",
        fillColor="#EEEEEE",
        padding=10,
        cornerRadius=10,
        orient="top-right",
    )

    alt.vconcat(
        add_ruler_as_selector_on_single_line_chart(
            world_agg_confirmed_chart,
            df_world_agg_confirmed,
            x_field=typedef.Columns.DATE,
            y_field=typedef.Columns.CONFIRMED,
        ),
        add_ruler_as_selector_on_single_line_chart(
            world_agg_growth_rate_chart,
            df_world_agg_growth_rate,
            x_field=typedef.Columns.DATE,
            y_field=typedef.Columns.GROWTH_RATE,
        ),
    ).save(viz_path, embed_options={"renderer": "svg"})


def add_ruler_as_selector_on_single_line_chart(
    chart: Any, df: pd.DataFrame, x_field: str, y_field: str
) -> Any:
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=[typedef.Columns.DATE],
        empty="none",
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(x=x_field, opacity=alt.value(0), tooltip=alt.Tooltip(y_field),)
        .add_selection(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = chart.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0)),
    )

    # # Draw text labels near the points, and highlight based on selection
    # text = chart.mark_text(align="left", dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, y_field, alt.value(" "))
    # )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(df)
        .mark_rule(color="gray")
        .encode(x=x_field)
        .transform_filter(nearest)
    )

    # Put the five layers into a chart and bind the data
    return alt.layer(chart, selectors, points, rules)


def create_viz_region_confirmed_and_rate(
    charts_path: str, dfs: Dict[str, pd.DataFrame]
) -> None:
    df_region_agg_confirmed = dfs["region-agg-confirmed"]
    df_region_agg_growth_rate = dfs["region-agg-growth-rate"]

    viz_path = os.path.join(charts_path, "region-agg-chart.html")

    choices = sorted(list(df_region_agg_confirmed["location"].unique()))
    input_dropdown = alt.binding_select(options=choices)
    single_selector = alt.selection_single(
        fields=[typedef.Columns.REGION],
        bind=input_dropdown,
        name="Location",
        init={typedef.Columns.REGION: choices[0]},
    )
    color = alt.condition(
        single_selector,
        alt.Color("%s:N" % typedef.Columns.REGION, legend=None),
        alt.value("lightgray"),
    )

    region_agg_confirmed_chart = (
        alt.Chart(df_region_agg_confirmed)
        .mark_line(point=True)
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.CONFIRMED, title="# New Cases"),
            color=color,
            tooltip=typedef.Columns.CONFIRMED,
        )
        .add_selection(single_selector)
        .transform_filter(single_selector)
    )

    region_agg_growth_rate_chart = (
        alt.Chart(df_region_agg_growth_rate)
        .mark_line(point=True)
        .encode(
            alt.X(typedef.Columns.DATE, title="Date"),
            alt.Y(typedef.Columns.GROWTH_RATE, title="Rate of New Cases"),
            color=color,
            tooltip=typedef.Columns.GROWTH_RATE,
        )
        .add_selection(single_selector)
        .transform_filter(single_selector)
    )

    alt.vconcat(region_agg_confirmed_chart, region_agg_growth_rate_chart).save(
        viz_path, embed_options={"renderer": "svg"}
    )


def add_ruler_to_multi_line_chart(
    df: pd.DataFrame, x: (str, str), category: (str, str), line: Any,
) -> Any:
    x_field, x_title = x
    category_field, category_title = category

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(
        type="single", nearest=True, on="mouseover", fields=[x_field], empty="none"
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = (
        alt.Chart(df)
        .mark_point()
        .encode(x=x_field, opacity=alt.value(0),)
        .add_selection(nearest)
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align="left", dx=5, dy=-5).encode(
        text=alt.condition(nearest, category_field, alt.value(" "))
    )

    # Draw a rule at the location of the selection
    rules = (
        alt.Chart(df)
        .mark_rule(color="gray")
        .encode(x=x_field)
        .transform_filter(nearest)
    )

    # Put the five layers into a chart and bind the data
    return alt.layer(line, selectors, points, rules, text)


def parse_args() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--data-path", required=True, help="Dir with processed data"
    )
    return arg_parser.parse_args()


def main(data_path: str):
    charts_path = os.path.join(data_path, "charts")
    if not os.path.exists(charts_path):
        os.makedirs(charts_path)
    dfs = preproc.read_proc_data(data_path)
    create_viz_growth_simulation(charts_path)
    create_viz_world_confirmed_and_rate(charts_path, dfs)
    create_viz_region_confirmed_and_rate(charts_path, dfs)


if __name__ == "__main__":
    args = parse_args()
    main(args.data_path)
