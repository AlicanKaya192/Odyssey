import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]
days = pd.to_datetime(["2024-03-14", "2024-06-20", "2024-10-08"])

# Kopya al, uc gunu NaN yap.


# Bir hafta oncesi ile sonrasinin ortalamasiyla doldur.


# Uc gunun yeni degerleri (liste).


# Tablo: visits, clean, repaired; satir sayisi ve repaired toplami.


# Standart sapma: once, sonra.


# Persembe ortalamasi: once, sonra.


# Iki kampanya gununun toplam etkisi.
