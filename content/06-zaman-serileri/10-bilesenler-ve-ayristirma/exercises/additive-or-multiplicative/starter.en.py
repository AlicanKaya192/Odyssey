import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

# Two models: additive and multiplicative, period=12.


# Absolute additive residual, mean by year: 2013, 2019, 2023.


# Additive residual: July 2013 and July 2023.


# Multiplicative residual as a percentage deviation; mean of the same years.


# The largest percentage deviation.


# The smallest and the largest seasonal factor: month and factor.
