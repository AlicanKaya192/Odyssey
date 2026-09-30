import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])

# lag_wrong: a plain shift(1). lag1: shift(1) within each shop.


# 2 January 2024, shop B: sales, lag_wrong, lag1 (a list).


# Shop B's sales on 1 January 2024.


# Correlations of sales with lag_wrong and with lag1 (three decimals).


# Number of NaN values in lag1.
