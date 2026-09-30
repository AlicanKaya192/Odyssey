import pandas as pd

w = pd.read_csv("two_walks.csv", index_col="date", parse_dates=True)

print(round(float(w["a"].corr(w["b"])), 3))

change = w.diff()
print(round(float(change["a"].corr(change["b"])), 3))

pieces = [(start, start + 100) for start in range(0, 500, 100)]

levels = []
for start, end in pieces:
    part = w.iloc[start:end]
    levels.append(round(float(part["a"].corr(part["b"])), 2))
print(levels)

changes = []
for start, end in pieces:
    part = change.iloc[start:end]
    changes.append(round(float(part["a"].corr(part["b"])), 2))
print(changes)
