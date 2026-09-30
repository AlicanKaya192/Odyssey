import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
visits = visits.asfreq("D")

classic = seasonal_decompose(visits, model="additive", period=7)
robust = STL(visits, period=7, robust=True).fit()

print(int(classic.trend.isna().sum()), int(robust.trend.isna().sum()))

spike = "2024-03-14"
before = "2024-03-13"
print(round(float(classic.trend.loc[spike])), round(float(robust.trend.loc[spike])))
print(round(float(classic.resid.loc[before])), round(float(robust.resid.loc[before])))
print(round(float(classic.resid.loc[spike])), round(float(robust.resid.loc[spike])))
