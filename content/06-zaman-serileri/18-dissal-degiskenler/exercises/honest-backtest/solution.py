import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")
cuts = [pd.Timestamp("2024-01-30") + pd.Timedelta(days=56 * i) for i in range(6)]


def plain(train, test):
    fit = ARIMA(train["sales"], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
    return fit.forecast(28).to_numpy()


def with_exog(train, test):
    columns = ["promo", "holiday", "temp_c"]
    fit = ARIMA(train["sales"], exog=train[columns], order=(1, 0, 0), seasonal_order=(0, 1, 1, 7)).fit()
    normal = train["temp_c"].groupby(train.index.dayofyear).mean()
    future = test[columns].copy()
    future["temp_c"] = [normal.get(day, normal.mean()) for day in test.index.dayofyear]
    return fit.forecast(28, exog=future).to_numpy()


results = {"plain": [], "exog": []}
for cut in cuts:
    train = c.loc[:cut]
    test = c.loc[cut + pd.Timedelta(days=1):].iloc[:28]
    actual = test["sales"].to_numpy()
    results["plain"].append(float(np.abs(actual - plain(train, test)).mean()))
    results["exog"].append(float(np.abs(actual - with_exog(train, test)).mean()))

for name, scores in results.items():
    print(name, round(float(np.mean(scores)), 2), round(float(np.max(scores)), 2))

wins = sum(e < p for e, p in zip(results["exog"], results["plain"]))
print(wins, round(1 - float(np.mean(results["exog"]) / np.mean(results["plain"])), 2))
