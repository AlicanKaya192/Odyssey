import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


# 13 deney: kesim gunu, MAE, yanlilik.


# Deney sayisi, ortalama, standart sapma, en kucuk, en buyuk.


# En kotu iki deneyin kesim gunleri.


# 5 Kasim deneyinin MAE'si ve ortalama yanlilik.


# Cubuk grafigi: chart.png.
