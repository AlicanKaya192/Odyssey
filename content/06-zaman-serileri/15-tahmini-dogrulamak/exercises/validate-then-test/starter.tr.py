import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def weeks_mean(train, h, k):
    pattern = train.iloc[-7 * k:].to_numpy().reshape(k, 7).mean(axis=0)
    return np.array([pattern[i % 7] for i in range(h)])


def score(k, some_cuts):
    values = []
    for cut in some_cuts:
        train = s.loc[:cut]
        test = s.loc[cut + pd.Timedelta(days=1):].iloc[:28]
        values.append(np.abs(test.to_numpy() - weeks_mean(train, 28, k)).mean())
    return float(np.mean(values))


# Dogrulama ve test kesimleri.


# k = 1..8 icin dogrulama MAE'si (liste).


# Dogrulamada en iyi k: k, dogrulama MAE, ayni k'nin test MAE'si.


# Hile: testte en iyi gorunen k ve test MAE'si.


# Iki test MAE'si arasindaki fark.
