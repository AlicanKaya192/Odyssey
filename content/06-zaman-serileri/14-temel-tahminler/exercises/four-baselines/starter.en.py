import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

train, test = s.iloc[:-28], s.iloc[-28:]
h = len(test)
future = test.index

# Four forecasts: mean_fc, naive_fc, snaive_fc, drift_fc.


# Mean absolute error of each (name and two decimals).


# The first test day: actual and the four forecasts.


# Chart: last 28 days of training + test (grey), four forecasts; chart.png.
