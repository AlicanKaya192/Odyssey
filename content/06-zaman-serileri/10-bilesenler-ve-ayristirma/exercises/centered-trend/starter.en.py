import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# The 7-day centred moving average.


# Number of NaN values.


# First and last date with a trend.


# The trend on those two dates (one decimal).


# The trailing mean; 25 December (centred) and 28 December (trailing).
