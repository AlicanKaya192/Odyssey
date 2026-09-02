import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})

by_name = data.set_index("name")

print(by_name.loc["Mina", "score"])
print(by_name.loc["Ada":"Mina", "score"])
print(by_name.loc["Kerem", "city"])
print(len(by_name.loc["Ada":"Mina"]))
