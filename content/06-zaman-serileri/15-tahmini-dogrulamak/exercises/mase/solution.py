import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]


def mase(actual, forecast, train, m):
    scale = np.mean(np.abs(train[m:] - train[:-m]))
    return float(np.mean(np.abs(actual - forecast)) / scale)


train = s.loc[:"2024-11-05"].to_numpy().astype(float)
actual = s.loc["2024-11-06":"2024-12-03"].to_numpy().astype(float)
snaive = np.array([train[-7:][i % 7] for i in range(28)])
mean_fc = np.full(28, train.mean())
print(round(mase(actual, snaive, train, 7), 2), round(mase(actual, mean_fc, train, 7), 2))

p_train = p.loc[:"2023"].to_numpy().astype(float)
p_actual = p.loc["2024"].to_numpy().astype(float)
copy = p.loc["2023"].to_numpy().astype(float)
growth = p.loc["2023"].sum() / p.loc["2022"].sum()
print(round(mase(p_actual, copy, p_train, 12), 2), round(mase(p_actual, copy * growth, p_train, 12), 2))

print(round(float(np.mean(np.abs(train[7:] - train[:-7]))), 2),
      round(float(np.mean(np.abs(p_train[12:] - p_train[:-12]))), 2))
