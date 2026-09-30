import numpy as np
import pandas as pd

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]
periods = [("2013", "2016"), ("2017", "2020"), ("2021", "2024")]

d = p.diff()
plain = [round(float(d.loc[a:b].std()), 1) for a, b in periods]
print(plain)

log_d = np.log(p).diff()
logged = [round(float(log_d.loc[a:b].std()), 3) for a, b in periods]
print(logged)

print(round(plain[-1] / plain[0], 2), round(logged[-1] / logged[0], 2))

growth = np.log(p).diff(12)
print(round(float(growth.mean() * 100), 1))
print(growth.dropna().index[0].date(), int(growth.isna().sum()))
