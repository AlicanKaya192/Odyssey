import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Adim 1: trend (7 gunluk ortalanmis ortalama).


# Adim 2: trendsiz seri, haftanin gunune gore ortalama, toplami sifir.


# Deseni yazdir (bir ondalik, liste).


# Deseni butun tarihlere yay.


# Adim 3: kalinti; kalintinin ve serinin standart sapmasi.


# 12 Mart 2024: gozlem, trend, mevsim, kalinti.


# Toplam seriyi geri veriyor mu?
