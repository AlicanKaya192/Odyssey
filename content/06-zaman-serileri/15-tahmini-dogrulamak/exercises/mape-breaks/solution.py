import numpy as np
import pandas as pd

long = pd.read_csv("stores_long.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales").asfreq("D")

a = wide["A"]
c = wide["C"].fillna(0)
print(int((c == 0).sum()))


def measures(y):
    actual = y.iloc[1:].to_numpy().astype(float)
    forecast = y.shift(1).iloc[1:].to_numpy().astype(float)
    error = np.abs(actual - forecast)
    mae = float(error.mean())
    with np.errstate(divide="ignore", invalid="ignore"):
        mape = float(np.mean(error / np.abs(actual)) * 100)
    scale = float((y - y.shift(7)).abs().mean())
    return round(mae, 2), round(mape, 2), round(mae / scale, 2)


print(measures(a))
print(measures(c))

print(round(abs(100 - 150) / 100 * 100, 1), round(abs(150 - 100) / 150 * 100, 1))
