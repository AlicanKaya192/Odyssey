import numpy as np
import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
v = v.astype(float)


def best_split(x, margin=14):
    # The k giving the smallest sum of squares, and the gain.
    pass


# Raw series: day of the change and the gain.


# Remove the weekend effect: ratio, adjusted; day of the change and the gain.


# Repair the three anomalies (clean): day, gain, before, after, percentage change.


# The gain of a second cut in the two pieces of clean.
