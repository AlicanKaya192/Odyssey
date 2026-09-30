import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

c = pd.read_csv("cafe_daily.csv", index_col="date", parse_dates=True).asfreq("D")

train = c.loc[:"2024-10-31"]
test = c.loc["2024-11-01":"2024-11-28"]
columns = ["promo", "holiday", "temp_c"]

# Dis degiskenli model ve 28 gunluk tahmin.


# Dis degiskensiz model ve 28 gunluk tahmin.


# Iki tahminin MAE'si (once degiskensiz).


# Test donemindeki kampanya gunleri.


# O gunlerde: gercek, degiskensiz tahmin, degiskenli tahmin.


# Grafik: chart.png.
