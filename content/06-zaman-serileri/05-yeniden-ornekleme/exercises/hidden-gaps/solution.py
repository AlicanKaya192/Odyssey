import pandas as pd

messy = pd.read_csv("sales_messy.csv", index_col="date", parse_dates=True)["sales"]
fixed = messy.sort_index().groupby(level=0).sum()

weekly = fixed.resample("W").agg(["sum", "count"])
print(int((weekly["count"] < 7).sum()))

week = weekly.loc["2024-07-21"]
print(int(week["sum"]), int(week["count"]))

mean = fixed.resample("W").mean().loc["2024-07-21"]
print(round(float(mean * 7)))

strict = fixed.asfreq("D").resample("W").sum(min_count=7)
print(int(strict.isna().sum()))
