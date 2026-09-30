import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

trend = s.rolling(7, center=True).mean()
print(int(trend.isna().sum()))

valid = trend.dropna()
print(valid.index[0].date(), valid.index[-1].date())
print(round(float(valid.iloc[0]), 1), round(float(valid.iloc[-1]), 1))

trailing = s.rolling(7).mean()
print(round(float(trend.loc["2024-12-25"]), 1), round(float(trailing.loc["2024-12-28"]), 1))
