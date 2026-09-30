import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
quarterly = s.groupby(s.index.to_period("Q")).sum()

for quarter, total in quarterly.loc["2024"].items():
    print(quarter, total)

q1 = quarterly.loc["2024Q1"]
q4 = quarterly.loc["2024Q4"]
print(round(float((q4 / q1 - 1) * 100), 1))

last_year = quarterly.loc["2023Q4"]
print(round(float((q4 / last_year - 1) * 100), 1))
