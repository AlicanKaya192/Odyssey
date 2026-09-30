import pandas as pd

orders = pd.read_csv("orders_raw.csv")

ordered = pd.to_datetime(orders["ordered_at"],
                         format="%d.%m.%Y %H:%M", errors="coerce")
delivered = pd.to_datetime(orders["delivered_on"], errors="coerce")

days = (delivered - ordered.dt.normalize()).dt.days

print(int(days.notna().sum()))
print(round(float(days.mean()), 2))
print(int(days.max()))
print(int((days > 3).sum()))
