import datetime
import math

import pandas as pd

from covid19 import typedef


def generate_infection_projection_data(
    start_date: datetime.date,
    end_date: datetime.date,
    starting_cases: int,
    growth_rate: float,
):
    entries = []
    days = (end_date - start_date + datetime.timedelta(days=1)).days

    for day in range(days):
        cases = int(starting_cases * math.pow(growth_rate, day))
        entries.append([day, cases, growth_rate])
    return pd.DataFrame(
        entries,
        columns=[
            typedef.Columns.DATE,
            typedef.Columns.CONFIRMED,
            typedef.Columns.GROWTH_RATE,
        ],
    )
