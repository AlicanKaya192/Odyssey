import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    X = pd.DataFrame(index=y.index)
    for k in (1, 2, 7, 14):
        X[f"lag{k}"] = y.shift(k)
    X["mean7"] = y.shift(1).rolling(7).mean()
    X["mean28"] = y.shift(1).rolling(28).mean()
    X["dow"] = y.index.dayofweek
    X["month"] = y.index.month
    return X


table = features(s).join(s.rename("y")).dropna()
columns = [c for c in table.columns if c != "y"]
train, test = table.loc[:"2023"], table.loc["2024"]

# Egitimdeki ve 2024'teki en yuksek y.


# Duzey uzerinde model; en yuksek tahmin.


# Test MAE: butun 2024 ve yalnizca Aralik.


# Hedef fark (y - lag7); ozellikler de lag7'ye gore.


# Fark modeli: tahmini duzeye cevir; ayni iki hata.


# Fark modelinin en yuksek tahmini.
