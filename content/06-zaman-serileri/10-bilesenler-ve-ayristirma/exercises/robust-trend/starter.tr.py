import pandas as pd
from statsmodels.tsa.seasonal import STL, seasonal_decompose

visits = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
visits = visits.asfreq("D")

# Klasik ayristirma (period=7).


# Dayanikli STL (period=7, robust=True).


# Trenddeki NaN sayilari: klasik, STL.


# 14 Mart trendi: klasik, STL.


# 13 Mart kalintisi: klasik, STL.


# 14 Mart kalintisi: klasik, STL.
