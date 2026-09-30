import pandas as pd
from statsmodels.tsa.stattools import adfuller

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
weather = pd.read_csv("weather.csv", index_col="date", parse_dates=True)

yearly = y.resample("YS").sum()
growth = (yearly.pct_change().dropna() * 100).round(1)
print(yearly.astype(int).tolist(), growth.tolist())

weekday = y.groupby(y.index.dayofweek).mean()
print(weekday.round().astype(int).tolist(), round(float(weekday[5] / weekday[0]), 2))

monthly = y.groupby(y.index.month).mean()
print(int(monthly.idxmax()), int(monthly.idxmin()),
      round(float(monthly.max() / monthly.min()), 2))

print(round(float(adfuller(y)[1]), 3), round(float(adfuller(y.diff().dropna())[1]), 3))

rainy = y[weather["rain"] == 1].mean()
dry = y[weather["rain"] == 0].mean()
print(round(float(rainy / dry), 2), round(float(y.corr(weather["temp_c"])), 2))
