import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

trend = s.rolling(365).mean()
print(int(trend.isna().sum()))

ends = [trend.loc[day] for day in ("2022-12-31", "2023-12-31", "2024-12-31")]
print(round(float(ends[0]), 1), round(float(ends[1]), 1), round(float(ends[2]), 1))

print(s.resample("YE").mean().round(1).tolist())
print(round(float(ends[2] - ends[1]), 1))
