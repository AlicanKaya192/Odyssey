import pandas as pd
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Klasik ayristirma (period=7).


# MSTL: periods=(7, 365).


# Mevsim tablosunun sutunlari.


# Kalintinin standart sapmasi: klasik, MSTL.


# Trendin aya gore ortalamasi: en yuksek - en dusuk (klasik, MSTL).


# MSTL trendinin ilk ve son degeri.


# Yillik mevsimin 2024'teki en yuksek ve en dusuk gunu.
