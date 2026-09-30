import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

# Monthly means.


# The index with May = 100.


# December index values (a dict, one decimal).


# Quarterly shares (%); the shares of the last quarter (a dict).


# A's share: last quarter minus first quarter (points, one decimal).
