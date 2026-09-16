import pandas as pd

data = pd.read_csv("students.csv")

below = data["score"] < 75
print(data.loc[below, "name"].tolist())

data.loc[below, "score"] = 75

print(int((data["score"] == 75).sum()))
print(round(data["score"].mean(), 2))
