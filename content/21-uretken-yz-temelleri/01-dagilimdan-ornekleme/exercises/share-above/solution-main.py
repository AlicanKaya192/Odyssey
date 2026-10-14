import numpy as np
from gen_data import make_fish

X, y = make_fish()
y = np.array(y)


def share_above(name, limit, n, seed):
    weights = X[y == name, 1]
    m, s = weights.mean(), weights.std(ddof=1)
    sim = np.random.default_rng(seed).normal(m, s, n)
    return [round(float((sim > limit).mean()), 4), round(float((weights > limit).mean()), 4)]


print(share_above("bream", 700, 100000, 9))
print(share_above("perch", 400, 100000, 9))
