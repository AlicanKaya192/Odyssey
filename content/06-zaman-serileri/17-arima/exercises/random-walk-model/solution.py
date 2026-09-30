import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
k = k.to_numpy()

orders = [(0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]

fits = {order: ARIMA(k, order=order).fit() for order in orders}
for order, fit in fits.items():
    print(order, round(float(fit.aic), 1))

aics = [float(fit.aic) for fit in fits.values()]
print(round(max(aics) - min(aics), 1))

names = fits[(1, 1, 1)].param_names
values = dict(zip(names, fits[(1, 1, 1)].params))
print(round(float(values["ar.L1"]), 2), round(float(values["ma.L1"]), 2))

forecast = fits[(0, 1, 0)].forecast(3)
print([round(float(v), 2) for v in forecast], round(float(k[-1]), 2))
