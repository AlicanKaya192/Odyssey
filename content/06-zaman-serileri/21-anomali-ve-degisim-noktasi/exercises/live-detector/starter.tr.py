import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
past = pd.concat([v.shift(7 * k) for k in (1, 2, 3, 4)], axis=1)


def alarms(expected):
    # Oransal sapmasi 0.25'i gecen gunler ("%m-%d" listesi).
    pass


# Ortancayla: alarm sayisi ve liste.


# Ortalamayla: alarm sayisi.


# Ortalamayla alarm veren, ortancayla vermeyen gunler.


# 21 Mart: ortalama beklenti, ortanca beklenti, gercek.
