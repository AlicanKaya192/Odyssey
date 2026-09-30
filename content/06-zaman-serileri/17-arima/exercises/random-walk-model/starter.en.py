import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
k = k.to_numpy()

orders = [(0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]

# Four candidates: order and AIC.


# Difference between the smallest and the largest AIC.


# (1, 1, 1): the AR and MA coefficients.


# (0, 1, 0): the 3-step forecast and the last value of the series.
