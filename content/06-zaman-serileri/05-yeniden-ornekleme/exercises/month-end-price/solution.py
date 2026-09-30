import pandas as pd

close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

month_sum = close.resample("ME").sum()
print(round(float(month_sum.loc["2024-03"].iloc[0]), 2))

month_last = close.resample("ME").last()
month_mean = close.resample("ME").mean()
march = month_last.loc["2024-03"].iloc[0]
print(round(float(march), 2), round(float(month_mean.loc["2024-03"].iloc[0]), 2))

bars = close.resample("ME").ohlc().loc["2024-03"].iloc[0]
print(round(float(bars["high"]), 2), round(float(bars["low"]), 2))

february = month_last.loc["2024-02"].iloc[0]
print(round(float((march / february - 1) * 100), 1))
