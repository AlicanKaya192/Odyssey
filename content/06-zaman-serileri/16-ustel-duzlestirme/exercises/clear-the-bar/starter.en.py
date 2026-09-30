import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


def backtest(forecast):
    scores = []
    for cut in cuts:
        train = s.loc[:cut]
        test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        scores.append(np.abs(test.to_numpy() - forecast(train, 28)).mean())
    return np.array(scores)


def hw(train, h):
    # The model with no trend and an additive season; h-day forecast (numpy array).
    pass


def hw_trend(train, h):
    # The same model with trend="add".
    pass


# Three methods: name, mean MAE, worst experiment.


# The snaive - hw difference: mean, standard deviation, wins of hw.


# The skill of hw.
