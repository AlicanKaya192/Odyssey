import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# Monthly totals of 2024 (month-start labels).


# The wrong way: resample("D").ffill(); row count and last date.


# The March total of the wrong series.


# The right way: divide by the number of days, spread over a full-year index.


# The March total of the right series (one decimal).


# 9 March 2024: the spread value and the real sales.
