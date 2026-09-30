import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

t = pd.read_csv("temperature_daily.csv", index_col="date", parse_dates=True)
t = t["temp_c"].asfreq("D")
anomaly = t - t.groupby(t.index.dayofyear).transform("mean")

# Training up to the end of 2023; the AR(1) model.


# The AR coefficient (phi).


# The last training value and the 5-day forecast.


# By hand: the last value x powers of phi.


# 2024, one day ahead: MAE for the mean (0), naive and AR(1).
