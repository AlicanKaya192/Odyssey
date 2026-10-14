import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def fit_gaussian(name):
    return {"mean": [], "cov": []}


result = fit_gaussian("perch")
print(result["mean"])
for row in result["cov"]:
    print(row)
