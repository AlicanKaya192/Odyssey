import pandas as pd

data = pd.DataFrame({
    "name": ["Ada", "Kerem", "Mina", "Deniz", "Efe"],
    "city": ["Ankara", "Izmir", "Ankara", "Bursa", "Ankara"],
    "score": [82, 74, 91, 68, 88],
})

ranked = data.sort_values("score", ascending=False)

print(ranked[["name", "score"]].head(3))
print(data.loc[data["score"].idxmax(), "name"])
print(list(ranked.index))
