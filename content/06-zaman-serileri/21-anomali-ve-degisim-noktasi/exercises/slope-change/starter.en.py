import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

s = pd.read_csv("subscribers.csv", index_col="date", parse_dates=True)["subscribers"]
t = np.arange(len(s))
y = s.to_numpy(dtype=float)

# A single line: the slope.


# Residual: first day, the largest, its day, last day.


# Look for the break: a line for each piece, the smallest sum of squares.


# 30 days ahead: with the single line and with the line of the last 60 days.


# Chart: the series, the single line, the two-piece line; chart.png.
