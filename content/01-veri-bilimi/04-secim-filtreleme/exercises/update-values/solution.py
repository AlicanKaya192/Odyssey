import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})

data.loc[data["score"] < 75, "score"] = 75

print(data[["name", "score"]])
print(int((data["score"] == 75).sum()))
print(round(data["score"].mean(), 2))
