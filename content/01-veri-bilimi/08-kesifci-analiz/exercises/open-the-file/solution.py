import pandas as pd

data = pd.read_csv("survey.csv")

print(data.shape)
print(data.dtypes.astype(str).tolist())
print(int(data.isna().sum().sum()))
print(data["city"].nunique())
