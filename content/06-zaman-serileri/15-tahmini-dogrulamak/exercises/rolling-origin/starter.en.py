import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def snaive(train, h):
    last = train.iloc[-7:].to_numpy()
    return np.array([last[i % 7] for i in range(h)], dtype=float)


# 13 experiments: cut day, MAE, bias.


# Number of experiments, mean, standard deviation, minimum, maximum.


# The cut days of the two worst experiments.


# MAE of the 5 November experiment and the mean bias.


# Bar chart: chart.png.
