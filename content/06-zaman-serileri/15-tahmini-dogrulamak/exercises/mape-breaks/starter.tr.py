import numpy as np
import pandas as pd

long = pd.read_csv("stores_long.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales").asfreq("D")

# A ve C magazalari; C'deki bosluklar sifir. C'de kac gun sifir?


def measures(y):
    # Naif tahmin (y.shift(1)) icin MAE, MAPE, MASE.
    pass


# A ve C icin sonuclar.


# MAPE simetrik degil: 100/150 ve 150/100.
