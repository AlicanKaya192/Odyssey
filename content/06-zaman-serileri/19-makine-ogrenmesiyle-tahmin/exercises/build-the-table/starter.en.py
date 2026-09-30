import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")


def features(y):
    # lag1, lag2, lag7, lag14, mean7, mean28, dow, month.
    pass


# The table: features + target (y), dropna; shape and first date.


# The column names.


# 10 March 2024: y, lag1, lag7, mean7.


# By hand: the mean of the sales of 3-9 March 2024.
