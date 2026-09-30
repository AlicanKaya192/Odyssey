import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

train, test = s.iloc[:-28], s.iloc[-28:]
h = len(test)
future = test.index

# Dort tahmin: mean_fc, naive_fc, snaive_fc, drift_fc.


# Her birinin ortalama mutlak hatasi (ad ve iki ondalik).


# Ilk test gunu: gercek ve dort tahmin.


# Grafik: egitimin son 28 gunu + test (gri), dort tahmin; chart.png.
