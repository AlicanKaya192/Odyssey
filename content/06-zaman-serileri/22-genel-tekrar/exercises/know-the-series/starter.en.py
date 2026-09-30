import pandas as pd
from statsmodels.tsa.stattools import adfuller

y = pd.read_csv("bike_clean.csv", index_col="date", parse_dates=True)["rentals"]
y = y.asfreq("D").astype(float)
weather = pd.read_csv("weather.csv", index_col="date", parse_dates=True)

# Yearly totals and the year-on-year percentage change.


# Weekday means; Saturday / Monday.


# The highest and the lowest month; their ratio.


# ADF p-value: level and first difference.


# Rainy / dry ratio; correlation with temperature.
