import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    # lag1, lag2, lag7, lag14, mean7, mean28, dow, month.
    pass


# Tablo: ozellikler + hedef (y), dropna; sekil ve ilk tarih.


# Sutun adlari.


# 10 Mart 2024: y, lag1, lag7, mean7.


# Elle: 3-9 Mart 2024 satislarinin ortalamasi.
