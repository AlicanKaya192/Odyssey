import pandas as pd
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")

classic = seasonal_decompose(s, model="additive", period=7)
fit = MSTL(s, periods=(7, 365)).fit()

print(fit.seasonal.columns.tolist())
print(round(float(classic.resid.std()), 2), round(float(fit.resid.std()), 2))


def swing(trend):
    by_month = trend.groupby(trend.index.month).mean()
    return round(float(by_month.max() - by_month.min()))


print(swing(classic.trend), swing(fit.trend))
print(round(float(fit.trend.iloc[0]), 1), round(float(fit.trend.iloc[-1]), 1))

yearly = fit.seasonal["seasonal_365"].loc["2024"]
print(yearly.idxmax().strftime("%m-%d"), yearly.idxmin().strftime("%m-%d"))
