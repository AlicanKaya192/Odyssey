import warnings

warnings.simplefilter("ignore")    # the KPSS out-of-table p-value warning

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def verdict(x):
    # ADF and KPSS p-values and the verdict: stationary / not stationary / mixed.
    pass


# The price.


# The difference of the price.


# ADF statistic and 5% critical value for the price.
