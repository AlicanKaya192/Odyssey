import pandas as pd
from orders_data import write_orders_csv

write_orders_csv("orders.csv", 20_000)
df = pd.read_csv("orders.csv")

numbers = df.select_dtypes("number")
text = df.select_dtypes(exclude="number")

numbers_bytes = numbers.memory_usage(deep=True, index=False).sum()
text_bytes = text.memory_usage(deep=True, index=False).sum()
total = numbers_bytes + text_bytes

print("numbers", round(numbers_bytes / total * 100, 1))
print("text", round(text_bytes / total * 100, 1))

print(round(total / len(df), 1))
