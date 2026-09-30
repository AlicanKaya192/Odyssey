import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

print(type(s.index).__name__)
print(s.loc["2024-03-09"])
print(s.loc["2024-03"].sum())
print(round(float(s.loc["2024"].mean()), 1))
