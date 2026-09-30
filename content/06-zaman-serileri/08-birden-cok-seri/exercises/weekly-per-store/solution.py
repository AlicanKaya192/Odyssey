import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])

weekly = long.groupby(["store", pd.Grouper(key="date", freq="W")])["sales"].sum()
print(len(weekly))
print(weekly.loc["A"].head(2).tolist())

for store in ["A", "B", "C", "D"]:
    series = weekly.loc[store]
    print(store, series.idxmax().strftime("%Y-%m-%d"), series.max())
