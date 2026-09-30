import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]

# Trendsiz, toplamsal mevsimli model.


# alfa ve gama.


# Son duzey.


# Son 7 mevsim payi.


# 28 gunluk tahmin; ilk 7 gun.


# MAE ve yanlilik.


# Grafik: chart.png.
