import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"]

# Mevsim normali ve sapma.


# Sapmanin ACF'si: ilk 5 gecikme.


# Sapmanin PACF'si: ilk 5 gecikme.


# r = 1. gecikmenin ACF'si; r'nin ilk 5 kuvveti.


# Ham sicaklik: 1. ve 365. gecikmenin ACF'si.
