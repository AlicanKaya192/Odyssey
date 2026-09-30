import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Bes tek adimli tahmin (sozluk).


# 2024 icin: ad, MAE, yanlilik.


# En iyi yontemin naife gore becerisi.


# Sizinti deneyi: bugunu de iceren dort haftalik ortalama ile MAE.
