import numpy as np

scores = np.array([80.0, np.nan, 90.0, 70.0, np.nan, 60.0])

missing = np.isnan(scores).sum()
average = np.nanmean(scores)

filled = scores.copy()
filled[np.isnan(filled)] = average

print(missing)
print(average)
print(filled)
print(round(filled.mean(), 2))
