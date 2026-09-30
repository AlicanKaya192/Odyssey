import numpy as np
import pandas as pd

truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
truth = truth.loc["2024"]

gap = truth.astype(float).copy()
gap.loc["2024-07-08":"2024-07-21"] = np.nan
days = gap[gap.isna()].index

linear = gap.interpolate()

chain = gap.copy()
for day in days:
    chain.loc[day] = chain.loc[day - pd.Timedelta(days=7)]


def error(filled):
    return round(float((filled.loc[days] - truth.loc[days]).abs().mean()), 1)


print(error(linear), error(chain))

for day in ("2024-07-13", "2024-07-20"):
    print(int(truth.loc[day]), round(float(linear.loc[day])), round(float(chain.loc[day])))

print(round(float(truth.loc[days].std()), 1), round(float(linear.loc[days].std()), 1),
      round(float(chain.loc[days].std()), 1))

print(int(gap.ffill(limit=3).isna().sum()))
