import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila", "Kaan", "Ela"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir", "Bursa", "Izmir"],
    "grade": ["A", "B", "A", "C", "B", "A", "B", "C"],
    "score": [82, 74, 91, 68, 88, 76, 70, 64],
})

table = data.pivot_table(
    index="city", columns="grade", values="score", aggfunc="mean"
)

print(table)
print(int(table.isna().sum().sum()))
print(table.loc["Ankara", "B"])
