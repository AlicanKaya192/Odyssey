import numpy as np
import pandas as pd

truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
truth = truth.loc["2024"]

gap = truth.astype(float).copy()
gap.loc["2024-07-08":"2024-07-21"] = np.nan
days = gap[gap.isna()].index

# Dogrusal doldurma.


# Haftalik zincir: her eksik gune 7 gun onceki deger.


# Bosluktaki ortalama mutlak hata: dogrusal, zincir.


# 13 ve 20 Temmuz: gercek, dogrusal, zincir.


# Bosluk icinde standart sapma: gercek, dogrusal, zincir.


# ffill(limit=3) sonrasi kalan NaN sayisi.
