import pandas as pd

data = pd.read_csv("students.csv")

print(data.groupby("city")["score"].mean().round(1).to_dict())

data["city_mean"] = data.groupby("city")["score"].transform("mean").round(1)
data["above"] = data["score"] > data["city_mean"]

print(data.loc[data["above"], "name"].tolist())
print(int(data["above"].sum()))
