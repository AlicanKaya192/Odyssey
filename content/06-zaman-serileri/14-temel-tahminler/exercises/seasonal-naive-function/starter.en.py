import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")


def seasonal_naive(train, h, m):
    # Repeat the last m values for h steps; the index is the h dates after training.
    pass


# Daily sales: m=7, h=10; the values (a list).


# First and last date of the same forecast.


# Monthly passengers (up to the end of 2023): m=12, h=12; the values (a list).


# Compare with 2024: MAE and bias.
