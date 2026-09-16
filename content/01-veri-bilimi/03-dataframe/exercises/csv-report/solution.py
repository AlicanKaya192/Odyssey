import pandas as pd

data = pd.read_csv("students.csv")
print(data.shape)

report = data.set_index("name")
print(report.loc["Mina", "score"])

counts = data["city"].value_counts()
print(counts.to_dict())
print(counts.idxmax())

print(int(data.isna().sum().sum()))
print(round(data["score"].mean(), 2), data["score"].max())
