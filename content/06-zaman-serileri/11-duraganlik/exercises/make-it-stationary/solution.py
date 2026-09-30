import warnings

warnings.simplefilter("ignore")

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss

p = pd.read_csv("passengers_monthly.csv", index_col="month", parse_dates=True)
p = p["passengers"]

versions = {
    "level": p,
    "diff": p.diff(),
    "diff12": p.diff(12),
    "log diff12": np.log(p).diff(12),
}

for name, x in versions.items():
    x = x.dropna()
    adf_p = float(adfuller(x)[1])
    kpss_p = float(kpss(x, regression="c", nlags="auto")[1])
    print(name, round(adf_p, 3), round(kpss_p, 3))

final = versions["log diff12"]
print(int(final.isna().sum()), round(float(final.std()), 3))

extra = final.diff()
print(round(float(extra.std()), 3))
