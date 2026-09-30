import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


def weeks_mean(train, h, k):
    pattern = train.iloc[-7 * k:].to_numpy().reshape(k, 7).mean(axis=0)
    return np.array([pattern[i % 7] for i in range(h)])


def errors(forecast):
    # The 28 days of absolute errors in each experiment; a 13 x 28 array.
    pass


# Error arrays for the two methods.


# Overall mean MAE: seasonal naive, four weeks.


# Difference by experiment: mean, standard deviation, wins of seasonal naive.


# Experiment 12 only (position 11).


# Error by week of the horizon: two lists.
