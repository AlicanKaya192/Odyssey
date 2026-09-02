import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe", "Sila"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara", "Izmir"],
    "score": [82, 74, 91, 68, 88, 76],
    "age": [21, 23, 22, 25, 21, 24],
})

print(data[data["city"].isin(["Izmir", "Bursa"])][["name", "city"]])
print(data[data["age"].between(21, 22)]["name"].tolist())
print(data[~data["city"].isin(["Ankara"])]["name"].tolist())
print(data.nlargest(2, "score")[["name", "score"]])
