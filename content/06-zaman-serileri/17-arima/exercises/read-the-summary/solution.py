import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]

big = ARIMA(train, order=(1, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()

weak = []
for name in big.params.index:
    if name == "sigma2":
        continue
    pvalue = float(big.pvalues[name])
    print(name, round(float(big.params[name]), 2), round(pvalue, 3))
    if pvalue > 0.05:
        weak.append(name)

print(weak)

small = ARIMA(train, order=(0, 1, 1), seasonal_order=(0, 1, 1, 7)).fit()
print(round(float(big.aic), 1), round(float(small.aic), 1))
print(round(float(big.resid.iloc[8:].std()), 2), round(float(small.resid.iloc[8:].std()), 2))
