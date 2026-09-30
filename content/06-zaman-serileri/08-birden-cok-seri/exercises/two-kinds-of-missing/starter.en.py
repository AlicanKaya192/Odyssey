import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

# Day names of the days on which C is NaN (distinct ones, a list).


# C: mean skipping NaN, and with fillna(0) (one decimal).


# D: the same two means.


# Daily total of the four shops: 30 April and 1 May.


# The total of A + B + C: the same two days.
