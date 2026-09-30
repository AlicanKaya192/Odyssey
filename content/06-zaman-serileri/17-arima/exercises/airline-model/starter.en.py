import warnings

warnings.simplefilter("ignore")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# (0,1,1)(0,1,1,12) on the logarithm.


# The two MA coefficients.


# The 12-month forecast (turned back with np.exp): MAE and percentage error.


# The same model without the logarithm: MAE.


# Residual check: drop the first 13 values, Ljung-Box (12 lags) p-value.


# August 2024: forecast and actual.


# Chart: chart.png.
