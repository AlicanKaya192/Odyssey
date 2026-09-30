import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)
load = load["load_mw"]

values = acf(load, nlags=200)

near = values[2:31]
lag = int(near.argmax()) + 2
print(lag, round(float(values[lag]), 2))

lag = int(near.argmin()) + 2
print(lag, round(float(values[lag]), 2))

far = values[100:201]
lag = int(far.argmax()) + 100
print(lag, round(float(values[lag]), 2))

print([round(float(values[lag]), 2) for lag in range(24, 169, 24)])
