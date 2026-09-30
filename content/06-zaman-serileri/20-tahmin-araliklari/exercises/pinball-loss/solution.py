import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)
past = error.loc["2023"]
base = s.shift(7).loc["2024"]
actual = s.loc["2024"]


def pinball(actual, forecast, q):
    diff = actual - forecast
    return float(np.mean(np.maximum(q * diff, (q - 1) * diff)))


for q in (0.5, 0.8, 0.9, 0.95):
    share = float(past.quantile(q))
    forecast = base + share
    loss = pinball(actual, forecast, q)
    rate = float((actual <= forecast).mean())
    print(q, round(share, 1), round(loss, 2), round(rate, 3))

print(round(pinball(actual, base, 0.9), 2))
