import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila", "Kaan", "Ela"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir", "Bursa", "Izmir"],
    "grade": ["A", "B", "A", "C", "B", "A", "B", "C"],
    "score": [82, 74, 91, 68, 88, 76, 70, 64],
})

report = data.groupby("city").agg(
    people=("name", "count"),
    average=("score", "mean"),
    highest=("score", "max"),
).round(1)

print(report)
print(report.loc["Izmir", "people"])
