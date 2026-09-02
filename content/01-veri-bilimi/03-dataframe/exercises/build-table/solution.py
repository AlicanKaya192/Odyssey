import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"],
    "score": [82, 74, 91, 68, 88],
})

print(data.shape)
print(list(data.columns))
print(data.head(2))
print(round(data["score"].mean(), 1))
