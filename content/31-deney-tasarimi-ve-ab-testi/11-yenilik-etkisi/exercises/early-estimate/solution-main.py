import numpy as np
from ab_data import make_novelty_test

new_first, old_last = [], []
for s in range(200, 220):
    t = make_novelty_test(n=10000, seed=s)
    t["week"] = (t["day"] - 1) // 7 + 1
    for is_new, week, store in [(True, 1, new_first), (False, 4, old_last)]:
        part = t[(t["is_new"] == is_new) & (t["week"] == week)]
        m = part.groupby("group")["clicks"].mean()
        store.append(m["B"] / m["A"] - 1)
print(round(float(np.mean(new_first)), 3), round(float(np.mean(old_last)), 3))
