import numpy as np
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# The seasonal difference.


# Number of lags beyond the band: series, d7 (21 lags).


# ACF of d7 at lags 1, 7 and 14.


# The lag of d7 with the largest absolute value, and its value.


# Save the correlogram of d7 as chart.png.
