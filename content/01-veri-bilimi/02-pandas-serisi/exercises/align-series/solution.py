import pandas as pd

first = pd.Series([40, 55, 70], index=["Ada", "Kerem", "Mina"])
second = pd.Series([30, 25, 60], index=["Mina", "Ada", "Kerem"])
extra = pd.Series([10], index=["Efe"])

total = first + second

print(total)
print(total.idxmax())

with_extra = total + extra
print(with_extra.isna().sum())
