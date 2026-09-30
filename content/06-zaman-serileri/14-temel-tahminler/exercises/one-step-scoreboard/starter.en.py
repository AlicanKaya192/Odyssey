import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Five one-step forecasts (a dictionary).


# For 2024: name, MAE, bias.


# Skill of the best method over naive.


# The leakage experiment: MAE with a four-week mean that includes today.
