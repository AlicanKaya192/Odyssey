import pandas as pd

table = pd.read_csv("store_sales.csv")
table["year"] = table["date"].str[:4]

means = table.groupby("year")["sales"].mean().round(1)
for year, value in means.items():
    print(year, value)

growth = (means.iloc[-1] / means.iloc[0] - 1) * 100
print(round(float(growth), 1))
