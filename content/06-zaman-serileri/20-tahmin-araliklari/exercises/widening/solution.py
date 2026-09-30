import numpy as np
import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

sd = float(k.diff().std())
print(round(sd, 3))

last = float(k.iloc[-1])
for h in (1, 10, 40):
    half = 1.96 * sd * np.sqrt(h)
    print(h, round(last - half, 1), round(last + half, 1))


def coverage(h, widen):
    error = (k.shift(-h) - k).dropna()
    bound = 1.96 * sd * np.sqrt(h) if widen else 1.96 * sd
    return round(float((error.abs() <= bound).mean()), 3)


for h in (1, 10, 40):
    print(h, coverage(h, True), coverage(h, False))
