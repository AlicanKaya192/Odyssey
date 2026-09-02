import pandas as pd

scores = pd.Series(
    [82, 74, 91, 68],
    index=["Ada", "Kerem", "Mina", "Deniz"],
)

print(scores)
print(scores["Mina"])
print(round(scores.mean(), 2))
print(scores.idxmax())
