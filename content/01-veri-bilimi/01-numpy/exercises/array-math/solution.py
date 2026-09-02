import numpy as np

prices = np.array([100, 250, 80, 400])
counts = np.array([3, 1, 5, 2])

totals = prices * counts
with_tax = totals * 1.2

print(totals)
print(np.round(with_tax, 1))
print(totals.sum())
