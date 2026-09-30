import pandas as pd
from sklearn.linear_model import LinearRegression

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

# Dogru tabloyla model: test MAE.


# Hatali tablo: mean7 = s.rolling(7).mean() (shift yok); test MAE.


# mean7 ile y korelasyonu: dogru tablo, hatali tablo.


# mean7 katsayisi: dogru model, hatali model.


# Hatali ozelligin 10 Mart 2024 degeri ve 4-10 Mart ortalamasi.
