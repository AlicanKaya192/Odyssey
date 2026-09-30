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
    fit = ExponentialSmoothing(train, seasonal="add", seasonal_periods=7).fit()
    return fit.forecast(h).to_numpy()


def hw_trend(train, h):
    fit = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7).fit()
    return fit.forecast(h).to_numpy()


results = {"snaive": backtest(snaive), "hw": backtest(hw), "hw trend": backtest(hw_trend)}

for name, scores in results.items():
    print(name, round(float(scores.mean()), 2), round(float(scores.max()), 2))

diff = results["snaive"] - results["hw"]
print(round(float(diff.mean()), 2), round(float(diff.std(ddof=1)), 2), int((diff > 0).sum()))

print(round(1 - float(results["hw"].mean() / results["snaive"].mean()), 2))
