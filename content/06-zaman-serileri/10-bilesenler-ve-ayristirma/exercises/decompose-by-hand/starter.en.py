import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Step 1: trend (7-day centred average).


# Step 2: detrended series, mean by day of the week, summing to zero.


# Print the pattern (one decimal, a list).


# Stretch the pattern over all the dates.


# Step 3: residual; standard deviation of the residual and of the series.


# 12 March 2024: observation, trend, seasonal, residual.


# Does the sum give the series back?
