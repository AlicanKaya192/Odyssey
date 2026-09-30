import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima.model import ARIMA

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

train = s.loc[:"2024-11-05"]
test = s.loc["2024-11-06":"2024-12-03"]

candidates = [
    ((0, 0, 0), (0, 1, 0, 7)),
    ((1, 0, 0), (0, 1, 1, 7)),
    ((0, 1, 1), (0, 1, 1, 7)),
    ((1, 1, 1), (0, 1, 1, 7)),
]

rows = []
for order, seasonal in candidates:
    fit = ARIMA(train, order=order, seasonal_order=seasonal).fit()
    check = acorr_ljungbox(fit.resid.iloc[8:], lags=[14])
    pvalue = float(check["lb_pvalue"].iloc[0])
    mae = float((test - fit.forecast(28)).abs().mean())
    rows.append((order, float(fit.aic), pvalue, mae))
    print(order, seasonal, round(float(fit.aic), 1), round(pvalue, 3), round(mae, 2))

best = min(rows, key=lambda row: row[1])
print(best[0])

print([row[0] for row in rows if row[2] > 0.05])
