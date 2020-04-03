import argparse
import datetime
import os.path
from typing import Dict, Set, List

import pandas as pd

from covid19 import constants
from covid19 import typedef


def generate_entries_spanning_period(
    start_date: datetime.date,
    end_date: datetime.date,
    values: Dict[datetime.date, Dict[str, int]],
    locations: Set[str],
) -> pd.DataFrame:
    days = (end_date - start_date + datetime.timedelta(days=1)).days
    entries = []
    # date / location / value
    for day in range(days):
        date = start_date + datetime.timedelta(day)
        for location in locations:
            entries.append([location, date, values[date][location]])
    return pd.DataFrame(data=entries, columns=["location", "date", "count"],)


def get_jhu_files(input_path: str) -> List[str]:
    return [
        os.path.join(input_path, file_name)
        for file_name in os.listdir(input_path)
        if file_name.endswith(".csv")
    ]


def read_jhu_log(file_path: str) -> pd.DataFrame:
    date = datetime.datetime.strptime(
        os.path.basename(file_path).rstrip(".csv"), "%m-%d-%Y"
    )
    df_daily = pd.read_csv(file_path)
    column_mapping = {
        column_name: column_name.replace("/", "_").replace(" ", "_")
        for column_name in df_daily.columns
    }
    df_daily = df_daily.rename(column_mapping, axis=1)
    df_daily = df_daily.rename(typedef.Columns.name_mapping(), axis=1)
    df_daily = df_daily[
        [
            typedef.Columns.REGION,
            typedef.Columns.CONFIRMED,
            typedef.Columns.RECOVERED,
            typedef.Columns.DEATHS,
        ]
    ]
    df_daily[typedef.Columns.DATE] = date

    for column_name, _type in typedef.Columns.type_mapping().items():
        if _type == "int64":
            df_daily[column_name] = df_daily[column_name].fillna(0)
        df_daily[column_name] = df_daily[column_name].astype(_type)
    return df_daily


def join_jhu_logs(input_path: str) -> pd.DataFrame:
    files = get_jhu_files(input_path)
    dfs = []
    for file_path in files:
        df_daily = read_jhu_log(file_path)
        dfs.append(df_daily)
    return pd.concat(dfs, axis=0)


def process_data_from_jhu(input_path: str, output_path: str) -> None:
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df_raw = join_jhu_logs(input_path)
    df_region_agg_confirmed = (
        df_raw.groupby([typedef.Columns.REGION, typedef.Columns.DATE])
        .sum()
        .reset_index()
    )
    df_region_agg_growth_rate = generate_regional_growth_rate_metrics(
        df_region_agg_confirmed
    )

    df_world_agg_confirmed = (
        df_region_agg_confirmed[[typedef.Columns.DATE, typedef.Columns.CONFIRMED]]
        .groupby([typedef.Columns.DATE])
        .sum()
        .reset_index()
    )

    df_world_agg_growth_rate = pd.DataFrame(
        {typedef.Columns.DATE: df_world_agg_confirmed[typedef.Columns.DATE]}
    )
    df_world_agg_growth_rate[typedef.Columns.GROWTH_RATE] = compute_rate_of_new_cases(
        df_world_agg_confirmed[typedef.Columns.CONFIRMED]
    )

    df_region_agg_confirmed.to_csv(
        os.path.join(output_path, constants.FILE_REGION_AGG_JHU_CONFIRMED),
        index=False,
        header=True,
    )
    df_region_agg_growth_rate.to_csv(
        os.path.join(output_path, constants.FILE_REGION_AGG_JHU_GROWTH_RATE),
        index=False,
        header=True,
    )
    df_world_agg_confirmed.to_csv(
        os.path.join(output_path, constants.FILE_WORLD_AGG_JHU_CONFIRMED),
        index=False,
        header=True,
    )
    df_world_agg_growth_rate.to_csv(
        os.path.join(output_path, constants.FILE_WORLD_AGG_JHU_GROWTH_RATE),
        index=False,
        header=True,
    )


def generate_regional_growth_rate_metrics(
    df_region_agg_confirmed: pd.DataFrame,
) -> pd.DataFrame:
    locations = set(df_region_agg_confirmed[typedef.Columns.REGION].unique())

    dfs = []
    for location in locations:
        df_location = df_region_agg_confirmed[
            df_region_agg_confirmed[typedef.Columns.REGION] == location
        ].copy()
        df_location = df_location.reset_index(drop=True)
        df_location[typedef.Columns.GROWTH_RATE] = compute_rate_of_new_cases(
            df_location[typedef.Columns.CONFIRMED]
        )
        dfs.append(df_location)
    df = pd.concat(dfs, axis=0)
    return df


def compute_rate_of_new_cases(count: pd.Series) -> pd.Series:
    growth_rate = count.astype(float) / pd.Series([0] + list(count.values[:-1])).astype(
        float
    )
    return growth_rate.map(lambda x: round(x, ndigits=3))


def read_proc_data(path: str) -> Dict[str, pd.DataFrame]:
    df_region_agg_confirmed = pd.read_csv(
        os.path.join(path, constants.FILE_REGION_AGG_JHU_CONFIRMED),
        header="infer",
        dtype={typedef.Columns.CONFIRMED: "int64", typedef.Columns.REGION: "category"},
        parse_dates=[typedef.Columns.DATE],
    )
    df_region_agg_growth_rate = pd.read_csv(
        os.path.join(path, constants.FILE_REGION_AGG_JHU_GROWTH_RATE),
        header="infer",
        dtype={
            typedef.Columns.CONFIRMED: "int64",
            typedef.Columns.GROWTH_RATE: "float64",
            typedef.Columns.REGION: "category",
        },
        parse_dates=[typedef.Columns.DATE],
    )
    df_world_agg_confirmed = pd.read_csv(
        os.path.join(path, constants.FILE_WORLD_AGG_JHU_CONFIRMED),
        header="infer",
        dtype={typedef.Columns.CONFIRMED: "int64"},
        parse_dates=[typedef.Columns.DATE],
    )
    df_world_agg_growth_rate = pd.read_csv(
        os.path.join(path, constants.FILE_WORLD_AGG_JHU_GROWTH_RATE),
        header="infer",
        dtype={
            typedef.Columns.CONFIRMED: "int64",
            typedef.Columns.GROWTH_RATE: "float64",
        },
        parse_dates=[typedef.Columns.DATE],
    )
    return {
        "region-agg-confirmed": df_region_agg_confirmed,
        "region-agg-growth-rate": df_region_agg_growth_rate,
        "world-agg-confirmed": df_world_agg_confirmed,
        "world-agg-growth-rate": df_world_agg_growth_rate,
    }


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "--input-path", required=True, help="Path to csv file with CV19 data"
    )
    arg_parser.add_argument(
        "--output-path", required=True, help="Dir to save csv with processed data"
    )
    return arg_parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_data_from_jhu(args.input_path, output_path=args.output_path)
