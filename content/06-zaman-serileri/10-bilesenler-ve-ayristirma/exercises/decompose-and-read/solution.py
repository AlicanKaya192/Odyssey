import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

result = seasonal_decompose(s, model="additive", period=7)
fig = result.plot()
fig.savefig("chart.png")

resid = result.resid
print(int(resid.isna().sum()), round(float(resid.std()), 2))

top = resid.abs().sort_values(ascending=False).head(3)
print(top.index.strftime("%Y-%m-%d").tolist())

day = top.index[0]
print(int(s.loc[day]), round(float(result.trend.loc[day]), 1),
      round(float(result.seasonal.loc[day]), 1), round(float(resid.loc[day]), 1))

by_day = resid.groupby(resid.index.dayofweek).mean()
print(round(float(by_day.abs().max()), 1))

by_month = result.trend.groupby(result.trend.index.month).mean()
print(int(by_month.idxmin()), round(float(by_month.min())),
      int(by_month.idxmax()), round(float(by_month.max())))
