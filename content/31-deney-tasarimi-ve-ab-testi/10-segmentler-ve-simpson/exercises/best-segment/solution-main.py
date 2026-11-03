import numpy as np
from ab_data import make_segment_test

keys = ["country", "platform", "group"]
best, overall = [], []
for s in range(500, 550):
    t = make_segment_test(n=20000, seed=s)
    cells = t.groupby(keys)["bought"].mean().unstack()
    best.append((cells["B"] / cells["A"] - 1).max())
    m = t.groupby("group")["bought"].mean()
    overall.append(m["B"] / m["A"] - 1)
print(round(float(np.mean(overall)), 3))
print(round(float(np.mean(best)), 3))
