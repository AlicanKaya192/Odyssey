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
    # The columns sin1, cos1, ..., sinK, cosK (by day of the year).
    pass


def calendar(index):
    # fourier(index, 2) + a dec column (day / 31 in December, otherwise 0).
    pass


# calendar(train.index): shape and column names.


# Two models: plain and with the calendar.


# The 28-day forecasts: name, MAE, bias.


# The dec coefficient.
