import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]
holidays = pd.to_datetime(pd.read_csv("holidays.csv")["date"])
start = y.index[0]


def features(index):
    x = pd.DataFrame(index=index)
    x["t"] = (index - start).days.to_numpy()
    for day in range(1, 7):
        x[f"d{day}"] = (index.dayofweek == day).astype(float)
    angle = 2 * np.pi * index.dayofyear.to_numpy() / 365.25
    x["s1"], x["c1"] = np.sin(angle), np.cos(angle)
    x["s2"], x["c2"] = np.sin(2 * angle), np.cos(2 * angle)
    x["holiday"] = index.isin(holidays).astype(float)
    return x


def log_model(train, index):
    model = LinearRegression().fit(features(train.index), np.log(train))
    return np.exp(model.predict(features(index)))


# The 13 x 28 array of relative errors.


# The mean and the 10% and 90% quantiles.


# For each experiment the interval from the other 12; the mean coverage.


# Fit on the whole series; forecast 1-28 January 2025; the total.


# The first day: forecast, lower end, upper end.


# Chart: the last 42 days, the forecast, the interval with fill_between; chart.png.
