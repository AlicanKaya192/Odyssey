import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


# 13 x 28 hata dizisi.


# Ilk 9 deney: kurmak; son 4 deney: sinamak.


# Her hafta icin %10 ve %90 yuzdelikleri (ilk 9 deneyden).


# Ayni haftalarda son 4 deneyin kapsamasi (liste).


# Son 4 deneyin toplam kapsamasi.
