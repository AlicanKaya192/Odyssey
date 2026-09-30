import pandas as pd

raw = pd.read_csv("sales_messy.csv", parse_dates=["date"])
full = raw.groupby("date")["sales"].sum().sort_index().asfreq("D")
truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Index of the missing days.


def score(filled):
    # Mean absolute error on the missing days (one decimal).
    pass


# Four methods: ffill, linear, week ago, both sides.


# For each: name and error.


# 10 February: the truth and the value of the four methods.
