import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import acf

load = pd.read_csv("energy_hourly.csv", index_col="timestamp", parse_dates=True)
load = load["load_mw"]

# The ACF, 200 lags.


# Highest among 2-30: lag and value.


# Lowest among 2-30: lag and value.


# Highest among 100-200: lag and value.


# ACF at the multiples of 24 (24, 48, ..., 168).
