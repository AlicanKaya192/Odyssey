import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
actual = s.loc["2024-11-06":"2024-12-03"].to_numpy().astype(float)

last_week = train.iloc[-7:].to_numpy()
forecast = np.array([last_week[i % 7] for i in range(28)], dtype=float)


def mae(actual, forecast):
    return float(np.mean(np.abs(actual - forecast)))


def rmse(actual, forecast):
    return float(np.sqrt(np.mean((actual - forecast) ** 2)))


def mape(actual, forecast):
    return float(np.mean(np.abs(actual - forecast) / np.abs(actual)) * 100)


def bias(actual, forecast):
    return float(np.mean(actual - forecast))


def report(forecast):
    print(round(mae(actual, forecast), 2), round(rmse(actual, forecast), 2),
          round(mape(actual, forecast), 2), round(bias(actual, forecast), 2))


report(forecast)
print(round(rmse(actual, forecast) / mae(actual, forecast), 2))

report(np.full(28, train.mean()))
