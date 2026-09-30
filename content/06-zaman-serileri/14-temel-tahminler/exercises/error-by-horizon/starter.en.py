import pandas as pd

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]
s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Share: naive error, h = 1, 5, 10, 20, 40 (two decimals, a list).


# Ratio of the 40-day to the 1-day error, and the square root of 40.


# Sales: seasonal naive error, w = 1, 2, 4, 8 weeks (one decimal, a list).


# Sales: plain naive error, h = 1, 3, 7 days (one decimal, a list).
