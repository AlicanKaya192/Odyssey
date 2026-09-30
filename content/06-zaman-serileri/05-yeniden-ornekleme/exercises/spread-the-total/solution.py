import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]

monthly = s.loc["2024"].resample("MS").sum()

wrong = monthly.resample("D").ffill()
print(len(wrong), wrong.index[-1].strftime("%Y-%m-%d"))
print(wrong.loc["2024-03"].sum())

per_day = monthly / monthly.index.days_in_month
idx = pd.date_range("2024-01-01", "2024-12-31", freq="D")
spread = per_day.reindex(idx, method="ffill")

print(round(float(spread.loc["2024-03"].sum()), 1))
print(round(float(spread.loc["2024-03-09"]), 1), s.loc["2024-03-09"])
