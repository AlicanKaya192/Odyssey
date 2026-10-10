import pandas as pd


def weekend_count(dates):
    days = pd.to_datetime(pd.Series(dates))
    return int((days.dt.dayofweek >= 6).sum())

print(weekend_count(["2026-03-06", "2026-03-07", "2026-03-08", "2026-03-09"]))
