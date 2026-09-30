import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-12-03"]
test = s.loc["2024-12-04":"2024-12-31"]


def fourier(index, K):
    day = index.dayofyear.to_numpy()
    columns = {}
    for k in range(1, K + 1):
        columns[f"sin{k}"] = np.sin(2 * np.pi * k * day / 365.25)
        columns[f"cos{k}"] = np.cos(2 * np.pi * k * day / 365.25)
    return pd.DataFrame(columns, index=index)


def calendar(index):
    table = fourier(index, 2)
    table["dec"] = np.where(index.month == 12, index.day / 31, 0.0)
    return table


X = calendar(train.index)
print(X.shape, X.columns.tolist())

plain = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()
rich = ARIMA(train, exog=X, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()

forecasts = {
    "plain": plain.forecast(28),
    "calendar": rich.forecast(28, exog=calendar(test.index)),
}

for name, forecast in forecasts.items():
    error = test - forecast
    print(name, round(float(error.abs().mean()), 2), round(float(error.mean()), 2))

print(round(float(rich.params["dec"]), 1))
