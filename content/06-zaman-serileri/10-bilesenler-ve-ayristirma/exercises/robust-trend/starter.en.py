import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
visits = visits.asfreq("D")

# Classical decomposition (period=7).


# Robust STL (period=7, robust=True).


# NaN counts in the trend: classical, STL.


# Trend on 14 March: classical, STL.


# Residual on 13 March: classical, STL.


# Residual on 14 March: classical, STL.
