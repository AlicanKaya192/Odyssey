import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
actual = s.loc["2024-11-06":"2024-12-03"].to_numpy().astype(float)

last_week = train.iloc[-7:].to_numpy()
forecast = np.array([last_week[i % 7] for i in range(28)], dtype=float)


def mae(actual, forecast):
    pass


def rmse(actual, forecast):
    pass


def mape(actual, forecast):
    pass


def bias(actual, forecast):
    pass


# Seasonal naive: MAE, RMSE, MAPE, bias.


# The RMSE / MAE ratio.


# The same four measures for the mean forecast.
