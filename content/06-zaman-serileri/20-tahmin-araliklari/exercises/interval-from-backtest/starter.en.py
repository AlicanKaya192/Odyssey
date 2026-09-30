import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


# The 13 x 28 array of errors.


# First 9 experiments: build; last 4: test.


# The 10% and 90% quantiles for each week (from the first 9).


# Coverage of the last 4 experiments in the same weeks (a list).


# Overall coverage of the last 4 experiments.
