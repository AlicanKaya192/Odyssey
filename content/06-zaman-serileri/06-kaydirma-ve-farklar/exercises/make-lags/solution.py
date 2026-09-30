import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

table = pd.DataFrame({
    "sales": s,
    "lag1": s.shift(1),
    "lag7": s.shift(7),
})

print(int(table["lag1"].isna().sum()), int(table["lag7"].isna().sum()))
print(table.loc["2024-03-09"].tolist())
print(round(float(table["sales"].corr(table["lag1"])), 3),
      round(float(table["sales"].corr(table["lag7"])), 3))
