import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("subscribers.csv", index_col="date", parse_dates=True)["subscribers"]
t = np.arange(len(s))
y = s.to_numpy(dtype=float)

# Tek dogru: egim.


# Kalinti: ilk gun, en buyuk, onun gunu, son gun.


# Kirilma gununu ara: iki parcaya ayri dogru, en kucuk kare toplami.


# 30 gun sonrasi: tek dogruyla ve son 60 gunun dogrusuyla.


# Grafik: seri, tek dogru, iki parcali dogru; chart.png.
