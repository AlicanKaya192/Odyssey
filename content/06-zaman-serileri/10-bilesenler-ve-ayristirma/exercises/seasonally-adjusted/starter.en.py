import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

# Multiplicative decomposition, period=12.


# The adjusted series.


# June-September 2024: raw values (a list).


# Same months: adjusted values (one decimal, a list).


# Percentage change in September 2024: raw and adjusted.


# Standard deviation of the monthly percentage change: raw and adjusted.
