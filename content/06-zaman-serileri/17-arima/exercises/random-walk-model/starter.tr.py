import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
k = k.to_numpy()

orders = [(0, 1, 0), (1, 1, 0), (0, 1, 1), (1, 1, 1)]

# Dort aday: mertebe ve AIC.


# En kucuk ile en buyuk AIC arasindaki fark.


# (1, 1, 1): AR ve MA katsayilari.


# (0, 1, 0): 3 adimlik tahmin ve serinin son degeri.
