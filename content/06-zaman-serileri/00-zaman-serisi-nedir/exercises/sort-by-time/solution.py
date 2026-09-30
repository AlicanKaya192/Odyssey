import pandas as pd

sales = pd.read_csv("sales_shuffled.csv")
sales = sales.sort_values("date").reset_index(drop=True)

print(sales["date"].iloc[0])
print(sales["date"].iloc[-1])
print(len(sales))
print(sales["sales"].head(3).tolist())
