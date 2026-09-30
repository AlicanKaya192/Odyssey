import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# 2024'un aylik toplamlari (ay basi etiketi).


# Yanlis yol: resample("D").ffill(); satir sayisi ve son tarih.


# Yanlis serideki Mart toplami.


# Dogru yol: gun sayisina bol, tam yil indeksine yay.


# Dogru serideki Mart toplami (bir ondalik).


# 9 Mart 2024: paylastirilmis deger ve gercek satis.
