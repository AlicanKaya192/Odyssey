import numpy as np
import pandas as pd

v = pd.read_csv("web_traffic.csv", index_col="date", parse_dates=True)["visits"]
v = v.astype(float)


def best_split(x, margin=14):
    x = np.asarray(x, dtype=float)
    total = ((x - x.mean()) ** 2).sum()
    best_k, best_sse = None, None
    for k in range(margin, len(x) - margin):
        left, right = x[:k], x[k:]
        sse = ((left - left.mean()) ** 2).sum() + ((right - right.mean()) ** 2).sum()
        if best_sse is None or sse < best_sse:
            best_k, best_sse = k, sse
    return best_k, 1 - best_sse / total


k, gain = best_split(v)
print(v.index[k].strftime("%Y-%m-%d"), round(float(gain), 2))

weekend = v.index.dayofweek >= 5
ratio = v[weekend].median() / v[~weekend].median()
print(round(float(ratio), 3))

adjusted = v.copy()
adjusted[weekend] = adjusted[weekend] / ratio
k, gain = best_split(adjusted)
print(adjusted.index[k].strftime("%Y-%m-%d"), round(float(gain), 2))

clean = adjusted.copy()
clean.loc[pd.to_datetime(["2024-03-14", "2024-06-20", "2024-10-08"])] = np.nan
clean = clean.interpolate()
k, gain = best_split(clean)
before = float(clean.iloc[:k].mean())
after = float(clean.iloc[k:].mean())
print(clean.index[k].strftime("%Y-%m-%d"), round(float(gain), 2), round(before), round(after),
      round((after / before - 1) * 100))

left_gain = best_split(clean.iloc[:k])[1]
right_gain = best_split(clean.iloc[k:])[1]
print(round(float(left_gain), 3), round(float(right_gain), 3))
