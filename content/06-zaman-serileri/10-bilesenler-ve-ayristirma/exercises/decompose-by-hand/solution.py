import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

trend = s.rolling(7, center=True).mean()

detrended = s - trend
pattern = detrended.groupby(detrended.index.dayofweek).mean()
pattern = pattern - pattern.mean()
print(pattern.round(1).tolist())

seasonal = pd.Series(pattern.loc[s.index.dayofweek].values, index=s.index)

resid = s - trend - seasonal
print(round(float(resid.std()), 2), round(float(s.std()), 2))

day = "2024-03-12"
print(int(s.loc[day]), round(float(trend.loc[day]), 1),
      round(float(seasonal.loc[day]), 1), round(float(resid.loc[day]), 1))

print(bool((trend + seasonal + resid - s).abs().max() < 1e-9))
