import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

daily_mean = s.resample("ME").mean()

mom = daily_mean.pct_change() * 100
yoy = daily_mean.pct_change(12) * 100

print(mom.round(1).loc["2024-01":"2024-04"].tolist())
print(yoy.round(1).loc["2024-01":"2024-04"].tolist())
print(round(float(yoy.loc["2024"].mean()), 1))
