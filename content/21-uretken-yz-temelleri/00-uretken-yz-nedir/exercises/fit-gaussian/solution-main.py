import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def fit_gaussian(name):
    part = X[y == name]
    mean = part.mean(axis=0)
    cov = np.cov(part, rowvar=False)
    return {"mean": mean.round(2).tolist(), "cov": cov.round(2).tolist()}


result = fit_gaussian("perch")
print(result["mean"])
for row in result["cov"]:
    print(row)
