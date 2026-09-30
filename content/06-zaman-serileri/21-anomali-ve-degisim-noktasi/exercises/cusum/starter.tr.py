import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
ref = v.loc["2024-01":"2024-02"]
profile = ref.groupby(ref.index.dayofweek).median()
rel = v / profile.reindex(v.index.dayofweek).to_numpy() - 1
sd = (ref / profile.reindex(ref.index.dayofweek).to_numpy() - 1).std()
z = rel / sd


def cusum(z, k, h):
    # Toplami biriktir; h'yi gecince gunu listeye ekle ve toplami sifirla.
    pass


# Kirpilmis seri, k = 1, h = 8: ilk alarm, 2 Eylul'den kac gun sonra, alarm sayisi.


# Kirpilmamis seri: ilk alarm.


# Kirpilmis seri, k = 0.5, h = 5: 2 Eylul'den onceki alarmlar.
