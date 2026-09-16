import pandas as pd

raw = pd.read_csv("students_raw.csv")

print(raw.shape)
print(raw.dtypes.astype(str).tolist())
print(int(raw.isna().sum().sum()))
print(int(raw.duplicated().sum()))
print(raw["city"].nunique())
