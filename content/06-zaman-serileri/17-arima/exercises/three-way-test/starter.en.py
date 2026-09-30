import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


def hw(train, h):
    fit = ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()
    return fit.forecast(h).to_numpy()


def backtest(forecast):
    scores = []
    for cut in cuts:
        train = s.loc[:cut]
        test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        scores.append(np.abs(test.to_numpy() - forecast(train, 28)).mean())
    return np.array(scores)


def arima(train, h):
    # The (0,1,1)(0,1,1,7) model; h-day forecast (numpy array).
    pass


# Three methods: name, mean MAE, worst experiment.


# snaive - arima: mean difference and the number of experiments ARIMA wins.


# hw - arima: mean, standard deviation, the number of experiments ARIMA wins.
