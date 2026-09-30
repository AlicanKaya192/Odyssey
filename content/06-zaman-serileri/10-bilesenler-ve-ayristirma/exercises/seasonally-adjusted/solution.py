import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

mul = seasonal_decompose(p, model="multiplicative", period=12)
adjusted = p / mul.seasonal

months = slice("2024-06", "2024-09")
print(p.loc[months].tolist())
print(adjusted.loc[months].round(1).tolist())

raw_change = p.pct_change() * 100
adj_change = adjusted.pct_change() * 100
print(round(float(raw_change.loc["2024-09-01"]), 1),
      round(float(adj_change.loc["2024-09-01"]), 1))

print(round(float(raw_change.std()), 1), round(float(adj_change.std()), 1))
