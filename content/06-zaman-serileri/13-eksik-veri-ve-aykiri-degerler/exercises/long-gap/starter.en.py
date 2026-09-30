import numpy as np
import pandas as pd

truth = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
truth = truth.loc["2024"]

gap = truth.astype(float).copy()
gap.loc["2024-07-08":"2024-07-21"] = np.nan
days = gap[gap.isna()].index

# Linear filling.


# The weekly chain: into each missing day the value from 7 days earlier.


# Mean absolute error within the gap: linear, chain.


# 13 and 20 July: truth, linear, chain.


# Standard deviation within the gap: truth, linear, chain.


# Number of NaN values left after ffill(limit=3).
