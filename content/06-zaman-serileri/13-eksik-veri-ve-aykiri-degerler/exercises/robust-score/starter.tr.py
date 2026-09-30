import pandas as pd

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)
visits = visits["visits"]

# Ortalama, ortanca, standart sapma.


# z-skoru; |z| > 3 olan gunler.


def robust(x):
    # Ortanca ve MAD'ye dayanan dayanikli puan.
    pass


# MAD.


# Dayanikli puani en buyuk 5 gun ve puanlari.


# 8 Ekim: z-skoru ve dayanikli puan.
