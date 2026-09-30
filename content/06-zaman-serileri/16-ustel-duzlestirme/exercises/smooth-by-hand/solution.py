import pandas as pd

s = pd.read_csv("store_sales.csv", index_col="date", parse_dates=True)["sales"]
s = s.asfreq("D")
y = s.loc["2024-09-01":"2024-09-14"]


def smooth(values, alpha):
    level = values[0]
    levels = []
    for value in values:
        level = alpha * value + (1 - alpha) * level
        levels.append(float(level))
    return levels


by_hand = smooth(y.to_numpy(), 0.5)
print([round(v, 1) for v in by_hand[:5]])

with_pandas = y.ewm(alpha=0.5, adjust=False).mean()
print([round(float(v), 1) for v in with_pandas.iloc[:5]])

print(bool(max(abs(a - b) for a, b in zip(by_hand, with_pandas)) < 1e-9))

print([round(smooth(y.to_numpy(), alpha)[-1], 1) for alpha in (0.1, 0.5, 0.9)])
print(int(s.loc["2024-09-15"]))
