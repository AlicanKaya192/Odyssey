import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

d7 = s.diff(7).dropna()


def count_outside(x):
    values = acf(x, nlags=21)[1:]
    band = 1.96 / np.sqrt(len(x))
    return int((np.abs(values) > band).sum())


print(count_outside(s), count_outside(d7))

values = acf(d7, nlags=21)
print([round(float(values[lag]), 2) for lag in (1, 7, 14)])

biggest = int(np.abs(values[1:]).argmax()) + 1
print(biggest, round(float(values[biggest]), 2))

fig = plot_acf(d7, lags=21)
fig.savefig("chart.png")
