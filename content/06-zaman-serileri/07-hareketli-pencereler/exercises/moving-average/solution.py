import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

ma7 = s.rolling(7).mean()
print(int(ma7.isna().sum()))

week = s.loc["2024-03-04":"2024-03-10"].mean()
print(round(float(ma7.loc["2024-03-10"]), 1), round(float(week), 1))

print(round(float(s.std()), 1), round(float(ma7.std()), 1))

ewm7 = s.ewm(span=7).mean()
print(round(float(ewm7.loc["2024-03-09"]), 1), round(float(ma7.loc["2024-03-09"]), 1))
