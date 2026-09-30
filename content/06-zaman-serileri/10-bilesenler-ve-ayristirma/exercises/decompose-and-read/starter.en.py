import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

# Additive decomposition, period=7.


# Save the chart as chart.png.


# NaN count and standard deviation of the residual.


# Dates of the three residuals largest in absolute value.


# The day of the largest residual: observation, trend, seasonal, residual.


# Mean of the residual by day of the week: the largest in absolute value.


# Mean of the trend by month: the lowest and the highest month.
