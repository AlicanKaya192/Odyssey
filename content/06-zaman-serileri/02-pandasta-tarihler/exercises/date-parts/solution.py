import pandas as pd

sales = pd.read_csv("store_sales.csv", parse_dates=["date"])

by_day = sales.groupby(sales["date"].dt.day_name())["sales"].mean()
by_day = by_day.sort_values(ascending=False)
for name, value in by_day.head(3).items():
    print(name, round(float(value), 1))

weekend = sales["date"].dt.dayofweek >= 5
share = sales.loc[weekend, "sales"].sum() / sales["sales"].sum() * 100
print(round(float(share), 1))

march = (sales["date"].dt.year == 2024) & (sales["date"].dt.month == 3)
print(int(sales.loc[march, "sales"].sum()))
