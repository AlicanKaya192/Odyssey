import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")


def seasonal_naive(train, h, m):
    # Son m degeri h adim boyunca tekrarla; indeks egitimden sonraki h tarih.
    pass


# Gunluk satis: m=7, h=10; degerler (liste).


# Ayni tahminin ilk ve son tarihi.


# Aylik yolcu (2023 sonuna kadar): m=12, h=12; degerler (liste).


# 2024 ile karsilastir: MAE ve yanlilik.
