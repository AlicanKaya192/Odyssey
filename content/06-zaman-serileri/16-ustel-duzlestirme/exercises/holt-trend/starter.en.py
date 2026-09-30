import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

annual = p.resample("YS").sum()
train, test = annual.iloc[:-2], annual.iloc[-2:]

# Three models: flat, additive, multiplicative.


# For each: name, two-year forecast (a list), MAE.


# The actual values (a list).


# Average yearly growth rate on the training data (percent).
