import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
adj = s - seasonal_decompose(s, period=7).seasonal

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def one_step_mae(x, alpha):
    # The level (ewm), tomorrow's forecast via shift(1), mean absolute error.
    pass


# The error for alpha = 0.05, 0.1, 0.2, 0.5, 1.0 (a list).


# Skill of the best alpha over naive.


# The alpha statsmodels finds: adjusted sales.


# The alpha statsmodels finds: share price.
