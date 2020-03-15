import argparse
import collections
import datetime
import os.path
from typing import Dict, Set

import pandas as pd

from covid19 import constants


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


def process_data_from_jhu(input_path: str, output_path: str):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    df_raw = pd.read_csv(input_path)
    df_raw = df_raw.drop(["Province/State", "Lat", "Long"], axis=1)
    df_region_agg_confirmed = df_raw.groupby(["Country/Region"]).sum().reset_index()
    df_region_agg_confirmed = df_region_agg_confirmed.melt(id_vars=["Country/Region"])
    df_region_agg_confirmed = df_region_agg_confirmed.rename(
        columns={"Country/Region": "location", "variable": "date", "value": "count"}
    )
    df_region_agg_confirmed["location"] = df_region_agg_confirmed["location"].astype(
        "category"
    )
    df_region_agg_confirmed["date"] = df_region_agg_confirmed["date"].astype(
        "datetime64"
    )
    df_region_agg_confirmed["count"] = df_region_agg_confirmed["count"].astype("int64")

    df_region_agg_growth_rate = generate_regional_growth_rate_metrics(
        df_region_agg_confirmed
    )

    df_world_agg_confirmed = (
        df_region_agg_confirmed[["date", "count"]].groupby(["date"]).sum().reset_index()
    )

    df_world_agg_growth_rate = pd.DataFrame({"date": df_world_agg_confirmed["date"]})
    df_world_agg_growth_rate["growth_rate"] = df_world_agg_confirmed["count"].astype(
        float
    ) / pd.Series([0] + list(df_world_agg_confirmed["count"].values[:-1])).astype(float)

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
    locations = set(df_region_agg_confirmed["location"].unique())

    dfs = []
    for location in locations:
        df_location = df_region_agg_confirmed[
            df_region_agg_confirmed["location"] == location
        ].copy()
        df_location = df_location.reset_index(drop=True)
        df_location["growth_rate"] = df_location["count"].astype(float) / pd.Series(
            [0] + list(df_location["count"].values[:-1])
        ).astype(float)
        dfs.append(df_location)

    df = pd.concat(dfs, axis=0)

    return df


def process_data_from_cs19se(input_path: str, output_path: str):
    """
    Expected format
    | count | location  |    date    |
    |   1   | Stockholm | 2020-01-01 |
    """
    df_source = pd.read_csv(
        input_path,
        header="infer",
        dtype={"count": "int64", "location": "category"},
        parse_dates=["date"],
    )
    start_date = df_source["date"].min()
    end_date = df_source["date"].max()
    locations = set(df_source["location"].unique())
    keys = {col: i for i, col in enumerate(df_source.columns)}
    values = collections.defaultdict(lambda: collections.defaultdict(int))
    for row in df_source.values:
        location = row[keys["location"]]
        date = row[keys["date"]]
        values[date][location] += row[keys["count"]]

    df_entries = generate_entries_spanning_period(
        start_date, end_date=end_date, values=values, locations=locations
    )
    df_agg = df_entries.loc[:, ["date", "count"]].groupby(["date"]).sum().reset_index()

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    df_agg["growth_rate"] = df_agg["count"].astype(float) / pd.Series(
        [0] + list(df_agg["count"].values[:-1])
    ).astype(float)
    df_agg.to_csv(
        os.path.join(output_path, constants.FILE_SE_AGG), index=False, header=True,
    )
    df_entries.to_csv(
        os.path.join(output_path, constants.FILE_SE_PROVINCE), index=False, header=True
    )


def read_proc_data(path: str):
    df_region_agg_confirmed = pd.read_csv(
        os.path.join(path, constants.FILE_REGION_AGG_JHU_CONFIRMED),
        header="infer",
        dtype={"count": "int64", "location": "category"},
        parse_dates=["date"],
    )
    df_region_agg_growth_rate = pd.read_csv(
        os.path.join(path, constants.FILE_REGION_AGG_JHU_GROWTH_RATE),
        header="infer",
        dtype={"count": "int64", "growth_rate": "float64", "location": "category"},
        parse_dates=["date"],
    )
    df_world_agg_confirmed = pd.read_csv(
        os.path.join(path, constants.FILE_WORLD_AGG_JHU_CONFIRMED),
        header="infer",
        dtype={"count": "int64"},
        parse_dates=["date"],
    )
    df_world_agg_growth_rate = pd.read_csv(
        os.path.join(path, constants.FILE_WORLD_AGG_JHU_GROWTH_RATE),
        header="infer",
        dtype={"count": "int64", "growth_rate": "float64"},
        parse_dates=["date"],
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