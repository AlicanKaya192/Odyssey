import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# naive: rolling(7).mean(); safe: shift(1) then rolling(7).mean().


# 9 March 2024: naive and safe (one decimal).


# Check by hand: the means of 3-9 March and of 2-8 March.


# Number of NaN values at the start of safe.


# For 7 days ahead: shift(7) then rolling(7).mean(); the value for 9 March 2024.
