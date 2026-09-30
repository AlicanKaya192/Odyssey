import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"].asfreq("MS")

train, test = p.loc[:"2023"], p.loc["2024"]

# The bar: 2023 x growth rate; MAE.


# Three models: add-add, add-mul, mul-mul.


# For each: name, MAE, percentage error.


# Skill of the best model over the bar.


# The three coefficients of the best model.


# August 2024: forecast of the best model and the actual value.
