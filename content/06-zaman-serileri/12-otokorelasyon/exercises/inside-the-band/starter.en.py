import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()


def outside(x, nlags=20):
    # Lag numbers beyond the band (lag 0 excluded).
    pass


# The band for the daily change (three decimals).


# Lags beyond the band for the daily change.


# Number of lags beyond the band for the price.


# ACF of the price at lags 1, 10 and 20.
