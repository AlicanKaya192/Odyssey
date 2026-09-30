import pandas as pd

close = pd.read_csv("stock_price.csv", index_col="date", parse_dates=True)["close"]

print(pd.infer_freq(close.index))
print(int(close.asfreq("D").isna().sum()), int(close.asfreq("B").isna().sum()))
print(len(close.loc["2024-03"]))

month_end = close.groupby(close.index.to_period("M")).last()
for month, value in month_end.loc["2024-01":"2024-03"].items():
    print(month, value)
