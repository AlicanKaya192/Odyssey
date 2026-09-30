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
    # sin1, cos1, ..., sinK, cosK sutunlari (yilin gunune gore).
    pass


def calendar(index):
    # fourier(index, 2) + dec sutunu (Aralik'ta gun / 31, yoksa 0).
    pass


# calendar(train.index): sekil ve sutun adlari.


# Iki model: yalin ve takvimli.


# 28 gunluk tahminler: ad, MAE, yanlilik.


# dec katsayisi.
