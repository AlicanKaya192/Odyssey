import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
day = pd.Timestamp("2024-03-09")

print(day.day_name(),
      (day - pd.Timedelta(days=365)).day_name(),
      (day - pd.Timedelta(days=364)).day_name())

growth_365 = (s / s.shift(365) - 1) * 100
growth_364 = (s / s.shift(364) - 1) * 100

print(round(float(growth_365.loc[day]), 1), round(float(growth_364.loc[day]), 1))
print(round(float(growth_365.loc["2024"].std()), 1),
      round(float(growth_364.loc["2024"].std()), 1))
