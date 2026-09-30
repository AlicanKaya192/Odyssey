import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

trailing = s.rolling(28).mean()
centered = s.rolling(28, center=True).mean()

part_c = centered.loc["2023-11-15":"2024-02-15"]
part_t = trailing.loc["2023-11-15":"2024-02-15"]

peak_c = part_c.idxmax()
peak_t = part_t.idxmax()
print(peak_c.strftime("%Y-%m-%d"))
print(peak_t.strftime("%Y-%m-%d"))
print((peak_t - peak_c).days)

print(round(float(part_c.max()), 1), round(float(part_t.max()), 1))
print(int(centered.iloc[-14:].isna().sum()), int(trailing.iloc[-14:].isna().sum()))
