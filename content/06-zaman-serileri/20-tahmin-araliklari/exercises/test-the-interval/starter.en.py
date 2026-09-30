import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
cuts = [pd.Timestamp("2024-01-02") + pd.Timedelta(days=28 * i) for i in range(13)]

# At each cut: model, 95% interval; inside or not (28 values) and mean width.


# Overall coverage.


# Coverage by experiment (a list).


# Cut days of the experiments with coverage below 0.8.


# With those removed: coverage and mean width.
