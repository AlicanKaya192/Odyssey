import pandas as pd
from statsmodels.tsa.stattools import acf, pacf

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"]

# The seasonal normal and the anomaly.


# ACF of the anomaly: first 5 lags.


# PACF of the anomaly: first 5 lags.


# r = ACF at lag 1; the first 5 powers of r.


# Raw temperature: ACF at lags 1 and 365.
