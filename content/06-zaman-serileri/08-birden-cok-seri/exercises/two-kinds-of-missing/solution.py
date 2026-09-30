import pandas as pd

long = pd.read_csv("stores.csv", parse_dates=["date"])
wide = long.pivot(index="date", columns="store", values="sales")

closed = wide.index[wide["C"].isna()]
print(closed.day_name().unique().tolist())

print(round(float(wide["C"].mean()), 1), round(float(wide["C"].fillna(0).mean()), 1))
print(round(float(wide["D"].mean()), 1), round(float(wide["D"].fillna(0).mean()), 1))

total = wide.sum(axis=1)
print(total.loc["2024-04-30"], total.loc["2024-05-01"])

same_set = wide[["A", "B", "C"]].sum(axis=1)
print(same_set.loc["2024-04-30"], same_set.loc["2024-05-01"])
