import numpy as np
from ab_data import make_population

users = make_population()
for col in ["load_ms", "minutes"]:
    x = users[col]
    print(col, round(x.mean(), 1))
# On each line, add the median, the standard deviation and the 95th
# percentile next to the mean (all with 1 place). Then print the name of
# the column whose mean and median differ the most.
