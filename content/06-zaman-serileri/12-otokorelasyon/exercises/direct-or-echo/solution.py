import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"]

normal = t.groupby(t.index.dayofyear).transform("mean")
anomaly = t - normal

a = acf(anomaly, nlags=5)
print([round(float(v), 2) for v in a[1:]])

pa = pacf(anomaly, nlags=5)
print([round(float(v), 2) for v in pa[1:]])

r = float(a[1])
print([round(r ** power, 2) for power in range(1, 6)])

raw = acf(t, nlags=365)
print(round(float(raw[1]), 2), round(float(raw[365]), 2))
