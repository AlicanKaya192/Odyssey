import numpy as np

scores = np.array([45, 82, 91, 60, 74, 38, 88])

passed = scores[scores >= 60]
middle = scores[(scores >= 60) & (scores < 85)]

print(passed)
print(len(passed))
print(round(passed.mean(), 2))
print(middle)
