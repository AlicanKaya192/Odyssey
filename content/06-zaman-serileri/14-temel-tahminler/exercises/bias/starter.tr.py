import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last_week = train.iloc[-7:].to_numpy()
    return [last_week[i % 7] for i in range(h)]


def evaluate(cut):
    # cut'a kadar egitim, sonraki 28 gun test; MAE, yanlilik, dusuk kalan gun sayisi.
    pass


# Iki deney: 5 Kasim ve 3 Aralik.


# 3 Aralik deneyi: hatanin haftalara gore ortalamasi (liste).
