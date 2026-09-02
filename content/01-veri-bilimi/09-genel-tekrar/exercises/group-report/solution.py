import pandas as pd

data = pd.DataFrame({
    "city": ["Ankara", "Izmir", "Ankara", "Bursa",
             "Izmir", "Ankara", "Bursa", "Izmir"],
    "score": [88, 62, 82, 45, 91, 70, 51, 84],
    "hours": [12, 5, 9, 2, 14, 7, 3, 11],
})

table = data.groupby("city")["score"].agg(["count", "mean", "std"]).round(2)

print(table)
print(round(data["score"].mean(), 2), data["score"].median())
print(table["count"].idxmin())
