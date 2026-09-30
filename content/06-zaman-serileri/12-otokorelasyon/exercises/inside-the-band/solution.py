import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
change = k.diff().dropna()


def outside(x, nlags=20):
    values = acf(x, nlags=nlags)
    band = 1.96 / np.sqrt(len(x))
    return [lag for lag in range(1, nlags + 1) if abs(values[lag]) > band]


print(round(float(1.96 / np.sqrt(len(change))), 3))
print(outside(change))
print(len(outside(k)))

values = acf(k, nlags=20)
print([round(float(values[lag]), 2) for lag in (1, 10, 20)])
