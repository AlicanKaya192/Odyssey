import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
y = s.loc["2024-09-01":"2024-09-14"]


def smooth(values, alpha):
    # Start the level at the first value; update at each value; return the levels.
    pass


# alpha = 0.5: the first 5 levels.


# The same with pandas: the first 5 values.


# Are the two results the same?


# Forecast for 15 September: alpha = 0.1, 0.5, 0.9.


# The actual value of 15 September.
