import warnings

warnings.simplefilter("ignore")    # the KPSS out-of-table p-value warning

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]

# Four series: level, diff, diff12, log diff12 (a dictionary).


# For each: name, ADF p, KPSS p.


# Rows lost and standard deviation of the last series.


# One unnecessary difference more: standard deviation.
