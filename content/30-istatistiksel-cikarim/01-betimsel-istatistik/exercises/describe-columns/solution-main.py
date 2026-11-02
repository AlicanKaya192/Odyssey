import numpy as np
from ab_data import make_population

users = make_population()
gaps = {}
for col in ["load_ms", "minutes"]:
    x = users[col]
    p95 = np.percentile(x, 95)
    print(col, round(x.mean(), 1), round(x.median(), 1),
          round(x.std(), 1), round(p95, 1))
    gaps[col] = abs(x.mean() - x.median())
print(max(gaps, key=gaps.get))
