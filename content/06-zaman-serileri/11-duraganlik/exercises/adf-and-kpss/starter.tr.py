import warnings

warnings.simplefilter("ignore")    # KPSS'in tablo disi p-degeri uyarisi

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def verdict(x):
    # ADF ve KPSS p-degerleri ve karar: stationary / not stationary / mixed.
    pass


# Fiyat.


# Fiyatin farki.


# Fiyat icin ADF istatistigi ve %5 kritik degeri.
