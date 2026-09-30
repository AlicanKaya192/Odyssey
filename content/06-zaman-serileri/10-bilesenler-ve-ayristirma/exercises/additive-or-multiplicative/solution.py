import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

add = seasonal_decompose(p, model="additive", period=12)
mul = seasonal_decompose(p, model="multiplicative", period=12)

size = add.resid.abs().groupby(add.resid.index.year).mean()
print(round(float(size.loc[2013]), 1), round(float(size.loc[2019]), 1),
      round(float(size.loc[2023]), 1))

print(round(float(add.resid.loc["2013-07-01"]), 1),
      round(float(add.resid.loc["2023-07-01"]), 1))

pct = (mul.resid - 1).abs() * 100
by_year = pct.groupby(pct.index.year).mean()
print(round(float(by_year.loc[2013]), 1), round(float(by_year.loc[2019]), 1),
      round(float(by_year.loc[2023]), 1))
print(round(float(pct.max()), 1))

factors = mul.seasonal.iloc[:12]
print(factors.idxmin().month, round(float(factors.min()), 3),
      factors.idxmax().month, round(float(factors.max()), 3))
