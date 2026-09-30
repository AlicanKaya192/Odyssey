import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Standard deviation: series, diff(), diff(7).


# NaN counts: series, diff(), diff(7).


# Mean by day of the week: highest - lowest (diff, diff(7)).


# Undo the plain difference and compare.


# Undo the seasonal difference by one step: computed and actual last value.
