import pandas as pd

sample = pd.Series(["09.03.2024", "10.03.2024", "11.03.2024"])

print(pd.to_datetime(sample).dt.month.tolist())
print(pd.to_datetime(sample, format="%d.%m.%Y").dt.month.tolist())

orders = pd.read_csv("orders.csv")
ordered = pd.to_datetime(orders["ordered_at"], format="%d.%m.%Y %H:%M")

print(ordered.min(), ordered.max())
print(ordered.dt.month.value_counts().sort_index().to_dict())
