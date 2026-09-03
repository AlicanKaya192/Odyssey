import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold, cross_val_score

df = pd.get_dummies(pd.read_csv("cars.csv").dropna(),
                    columns=["fuel", "gearbox"])
X = df.drop(columns=["price"])
y = df["price"]

kf = KFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(LinearRegression(), X, y, cv=kf,
                         scoring="neg_mean_absolute_error")

errors = [round(float(-s), 2) for s in scores]
mean = sum(errors) / len(errors)
spread = (sum((e - mean) ** 2 for e in errors) / len(errors)) ** 0.5

print(errors)
print(round(mean, 2), round(spread, 2))
print("inside" if min(errors) <= 17.07 <= max(errors) else "outside")
