import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

w = pd.read_csv("two_processes.csv", index_col="date", parse_dates=True)


def first_lags(values):
    return [round(float(v), 2) for v in values[1:]]


for name in ("x", "y"):
    print(first_lags(acf(w[name], nlags=4)))
    print(first_lags(pacf(w[name], nlags=4)))


def kind(series):
    band = 1.96 / np.sqrt(len(series))
    second = acf(series, nlags=2)[2]
    if abs(second) < band:
        return "MA"
    return "AR"


print(kind(w["x"]), kind(w["y"]))
