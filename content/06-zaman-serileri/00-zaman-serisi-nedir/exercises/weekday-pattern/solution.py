import pandas as pd

table = pd.read_csv("store_sales_days.csv")
means = table.groupby("weekday")["sales"].mean().sort_values()

print(means.index[-1], round(float(means.iloc[-1]), 1))
print(means.index[0], round(float(means.iloc[0]), 1))
print(round(float(means.iloc[-1] / means.iloc[0]), 2))
