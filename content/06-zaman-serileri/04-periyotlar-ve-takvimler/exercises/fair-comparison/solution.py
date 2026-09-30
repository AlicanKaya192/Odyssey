import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
monthly = s.groupby(s.index.to_period("M")).sum()

feb = monthly.loc["2024-02"]
mar = monthly.loc["2024-03"]
print(feb, mar)

feb_days = pd.Period("2024-02", "M").days_in_month
mar_days = pd.Period("2024-03", "M").days_in_month
print(feb_days, mar_days)

feb_mean = round(float(feb / feb_days), 1)
mar_mean = round(float(mar / mar_days), 1)
print(feb_mean, mar_mean)

print("February" if feb_mean > mar_mean else "March")
