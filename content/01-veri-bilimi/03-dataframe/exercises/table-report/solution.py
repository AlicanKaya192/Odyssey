import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"],
    "score": [82, 74, 91, 68, 88],
})

report = data.set_index("name")

print(report.loc["Mina", "score"])
print(data["city"].value_counts())
print(data["city"].value_counts().idxmax())
print(int(data.isna().sum().sum()))
print(round(data["score"].mean(), 2), data["score"].max())
