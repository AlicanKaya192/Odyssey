import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])

long["lag_wrong"] = long["sales"].shift(1)
long["lag1"] = long.groupby("store")["sales"].shift(1)

row = long[(long["date"] == "2024-01-02") & (long["store"] == "B")].iloc[0]
print([int(row["sales"]), float(row["lag_wrong"]), float(row["lag1"])])

first = long[(long["date"] == "2024-01-01") & (long["store"] == "B")].iloc[0]
print(int(first["sales"]))

print(round(float(long["sales"].corr(long["lag_wrong"])), 3),
      round(float(long["sales"].corr(long["lag1"])), 3))
print(int(long["lag1"].isna().sum()))
