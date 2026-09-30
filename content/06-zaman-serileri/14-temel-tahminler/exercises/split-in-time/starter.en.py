import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
s = s.loc[:"2024-12-03"]

# The last 28 days are the test, the rest the training.


# The lengths.


# Last date of the training, first date of the test.


# The horizon and the index of the future dates.


# First and last date of the index.


# Is the index the same as the index of the test?


# Mean of training and test.
