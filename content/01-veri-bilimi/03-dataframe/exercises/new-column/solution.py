import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"],
    "score": [82, 74, 91, 68, 88],
})

data["passed"] = data["score"] >= 75
data["bonus"] = data["score"] + 10

print(data[["name", "score", "passed", "bonus"]])
print(int(data["passed"].sum()))
