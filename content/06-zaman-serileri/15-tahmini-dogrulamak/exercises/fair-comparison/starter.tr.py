import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


def weeks_mean(train, h, k):
    pattern = train.iloc[-7 * k:].to_numpy().reshape(k, 7).mean(axis=0)
    return np.array([pattern[i % 7] for i in range(h)])


def errors(forecast):
    # Her deneyde 28 gunluk mutlak hatalar; 13 x 28 dizi.
    pass


# Iki yontem icin hata dizileri.


# Genel ortalama MAE: mevsimsel naif, dort hafta.


# Deney deney fark: ortalama, standart sapma, mevsimsel naifin kazandigi deney.


# Yalnizca 12. deney (konum 11).


# Ufkun haftasina gore hata: iki liste.
