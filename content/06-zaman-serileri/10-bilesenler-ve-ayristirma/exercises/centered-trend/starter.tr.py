import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# 7 gunluk ortalanmis hareketli ortalama.


# NaN sayisi.


# Trendin dolu oldugu ilk ve son tarih.


# O iki tarihteki trend (bir ondalik).


# Geriye donuk ortalama; 25 Aralik (ortalanmis) ve 28 Aralik (geriye donuk).
