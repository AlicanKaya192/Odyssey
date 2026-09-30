import pandas as pd

sales = pd.read_csv("store_sales.csv")
sales["date"] = pd.to_datetime(sales["date"])

print(pd.api.types.is_datetime64_any_dtype(sales["date"]))

first = sales["date"].min()
last = sales["date"].max()
print(first.strftime("%Y-%m-%d"), last.strftime("%Y-%m-%d"))
print((last - first).days)
print(first.day_name())
