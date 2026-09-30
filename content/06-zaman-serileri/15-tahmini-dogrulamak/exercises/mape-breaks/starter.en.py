import numpy as np
import pandas as pd

long = pd.read_csv("stores_long.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales").asfreq("D")

# Shops A and C; gaps in C are zero. How many zero days in C?


def measures(y):
    # MAE, MAPE, MASE for the naive forecast (y.shift(1)).
    pass


# Results for A and C.


# MAPE is not symmetric: 100/150 and 150/100.
