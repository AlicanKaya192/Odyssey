import pandas as pd
from statsmodels.tsa.stattools import acf

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

# By hand: s.corr(s.shift(k)) for lags 1..7 (two decimals, a list).


# With acf: lag 0 excluded (two decimals, a list).


# The lag of the highest value.


# Length of the acf array and its first element.
