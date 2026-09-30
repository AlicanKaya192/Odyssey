import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

week = s.loc["2024-03-04":"2024-03-10"]
print(len(week), week.sum())

quarter = s.loc["2024-01":"2024-03"]
print(len(quarter), quarter.sum())

print(round(float(s.loc["2024-12"].mean()), 1))

best = s.loc["2024"].idxmax()
print(best.strftime("%Y-%m-%d"), s.loc[best])
