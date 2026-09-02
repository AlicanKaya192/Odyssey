import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"],
    "score": [82, 74, 91, 68, 88],
})

subset = data[["name", "score"]]

print(subset)
print(type(data["score"]).__name__)
print(type(data[["score"]]).__name__)
