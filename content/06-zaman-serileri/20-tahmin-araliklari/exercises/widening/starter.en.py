import numpy as np
import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

# Standard deviation of the daily change.


# The 95% interval from the last value for h = 1, 10, 40.


def coverage(h, widen):
    # The error h days later from every day; the share within the bound.
    pass


# h = 1, 10, 40: coverage with the square root rule and with a constant width.
