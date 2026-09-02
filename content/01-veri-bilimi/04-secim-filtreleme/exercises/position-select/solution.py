import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})

print(data.iloc[0, 0])
print(data.iloc[1:3][["name", "score"]])
print(data.iloc[:, [0, 2]].head(3))
print(data.iloc[-1]["name"])
