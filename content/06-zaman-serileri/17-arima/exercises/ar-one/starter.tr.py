import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"].asfreq("D")
anomaly = t - t.groupby(t.index.dayofyear).transform("mean")

# Egitim 2023 sonuna kadar; AR(1) modeli.


# AR katsayisi (phi).


# Egitimin son degeri ve 5 gunluk tahmin.


# Elle: son deger x phi'nin kuvvetleri.


# 2024, bir gun sonrasi: ortalama (0), naif, AR(1) icin MAE.
