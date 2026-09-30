import warnings

warnings.simplefilter("ignore")

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.seasonal import seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
adj = s - seasonal_decompose(s, period=7).seasonal

k = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]


def one_step_mae(x, alpha):
    forecast = x.ewm(alpha=alpha, adjust=False).mean().shift(1)
    return float((x - forecast).abs().iloc[1:].mean())


alphas = (0.05, 0.1, 0.2, 0.5, 1.0)
errors = [one_step_mae(adj, alpha) for alpha in alphas]
print([round(e, 2) for e in errors])

print(round(1 - min(errors) / errors[-1], 2))

fit = ExponentialSmoothing(adj).fit()
print(round(float(fit.params["smoothing_level"]), 2))

fit = ExponentialSmoothing(k.to_numpy()).fit()
print(round(float(fit.params["smoothing_level"]), 2))
