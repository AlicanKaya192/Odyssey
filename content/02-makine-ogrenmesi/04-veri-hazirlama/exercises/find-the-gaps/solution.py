import pandas as pd

df = pd.read_csv("cars.csv")
missing = df.isna().sum()

print(len(df))
print([f"{name}:{int(count)}" for name, count in missing.items() if count > 0])
print(df.select_dtypes(exclude="number").columns.tolist())
print(sorted(df["fuel"].unique().tolist()))
