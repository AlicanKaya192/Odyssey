import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# Logaritma uzerinde (0,1,1)(0,1,1,12).


# Iki MA katsayisi.


# 12 aylik tahmin (np.exp ile geri cevir): MAE ve yuzde hata.


# Ayni model logaritmasiz: MAE.


# Kalinti denetimi: ilk 13 degeri at, Ljung-Box (12 gecikme) p-degeri.


# Agustos 2024: tahmin ve gercek.


# Grafik: chart.png.
