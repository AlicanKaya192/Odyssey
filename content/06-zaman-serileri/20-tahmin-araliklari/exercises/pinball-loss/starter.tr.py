import numpy as np
import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

error = s - s.shift(7)
past = error.loc["2023"]
base = s.shift(7).loc["2024"]
actual = s.loc["2024"]


def pinball(actual, forecast, q):
    pass


# q = 0.5, 0.8, 0.9, 0.95: pay, pinball kaybi, altinda kalma orani.


# q = 0.9 iken nokta tahminin (base) pinball kaybi.
