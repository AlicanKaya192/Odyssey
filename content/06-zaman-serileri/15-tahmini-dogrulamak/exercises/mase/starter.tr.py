import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]


def mase(actual, forecast, train, m):
    pass


# Gunluk satis: egitim, test, iki tahmin; MASE.


# Aylik yolcu: egitim, test, iki tahmin; MASE.


# Iki serinin olcegi (payda).
