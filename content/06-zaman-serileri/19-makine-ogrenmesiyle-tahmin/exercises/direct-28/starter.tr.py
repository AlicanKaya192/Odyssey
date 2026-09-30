import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]


def safe_features(full, calendar=True):
    X = pd.DataFrame(index=full.index)
    for k in (28, 35, 42, 56):
        X[f"lag{k}"] = full.shift(k)
    X["mean_4w"] = (full.shift(28) + full.shift(35) + full.shift(42) + full.shift(49)) / 4
    X["level28"] = full.shift(28).rolling(28).mean()
    for day in range(1, 7):
        X[f"d{day}"] = (X.index.dayofweek == day).astype(float)
    if calendar:
        doy = X.index.dayofyear.to_numpy()
        X["t"] = np.arange(len(X))
        X["dec"] = np.where(X.index.month == 12, X.index.day / 31, 0.0)
        for k in (1, 2):
            X[f"sin{k}"] = np.sin(2 * np.pi * k * doy / 365.25)
            X[f"cos{k}"] = np.cos(2 * np.pi * k * doy / 365.25)
    return X


def forecast(train, future_index, calendar):
    # Gelecegi NaN olarak ekle, ozellikleri kur, dogrusal model, tahmin.
    pass


# 13 deney, iki surum: her deneyin MAE'si.


# Her surum: ad, ortalama MAE, en kotu deney.


# Takvimli surumun mevsimsel naife (17.95) gore becerisi.
