import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Trailing and centred 28-day means.


# Peak dates in 2023-11-15 .. 2024-02-15 (centred first).


# The difference between the two dates in days.


# The values of the two peaks (one decimal).


# NaN counts in the last 14 days (centred first).
