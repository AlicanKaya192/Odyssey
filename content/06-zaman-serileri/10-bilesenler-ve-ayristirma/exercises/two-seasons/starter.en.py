import pandas as pd
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Classical decomposition (period=7).


# MSTL: periods=(7, 365).


# Columns of the seasonal table.


# Standard deviation of the residual: classical, MSTL.


# Mean of the trend by month: highest - lowest (classical, MSTL).


# First and last value of the MSTL trend.


# Highest and lowest day of the yearly season in 2024.
