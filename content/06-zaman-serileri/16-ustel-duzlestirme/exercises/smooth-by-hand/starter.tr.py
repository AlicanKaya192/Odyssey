import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
y = s.loc["2024-09-01":"2024-09-14"]


def smooth(values, alpha):
    # Duzeyi ilk degerle baslat; her degerde guncelle; duzeyleri dondur.
    pass


# alfa = 0.5: ilk 5 duzey.


# pandas ile ayni hesap: ilk 5 deger.


# Iki sonuc ayni mi?


# 15 Eylul tahmini: alfa = 0.1, 0.5, 0.9.


# 15 Eylul'un gercek degeri.
