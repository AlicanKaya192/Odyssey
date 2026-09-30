import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# The one-day-ahead error; 2023 (past) and 2024 (future).


# The 10% and 90% quantiles of past.


# 15 March 2024: forecast, lower end, upper end, actual.


def coverage(level):
    # Two quantiles from past; the share of future errors inside.
    pass


# Coverage: 0.5, 0.8, 0.95.
