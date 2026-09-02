import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})

selected = data[(data["score"] >= 80) & (data["city"] == "Ankara")]

print(selected[["name", "score"]])
print(len(selected))
print(round(selected["score"].mean(), 2))
print(list(selected.index))
