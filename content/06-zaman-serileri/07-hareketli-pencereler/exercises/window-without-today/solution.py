import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

naive = s.rolling(7).mean()
safe = s.shift(1).rolling(7).mean()

print(round(float(naive.loc["2024-03-09"]), 1), round(float(safe.loc["2024-03-09"]), 1))
print(round(float(s.loc["2024-03-03":"2024-03-09"].mean()), 1),
      round(float(s.loc["2024-03-02":"2024-03-08"].mean()), 1))

print(int(safe.isna().sum()))

week_ahead = s.shift(7).rolling(7).mean()
print(round(float(week_ahead.loc["2024-03-09"]), 1))
