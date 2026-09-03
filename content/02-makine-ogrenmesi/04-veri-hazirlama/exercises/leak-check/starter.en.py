import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
X = pd.DataFrame(rng.normal(size=(80, 300)),
                 columns=[f"c{i}" for i in range(300)])
y = pd.Series(rng.normal(size=80))

# Write the remaining imports.


# THE LEAKY PATH
# Compute each column's absolute correlation with the target on all the
# data. Select the top five, THEN split, train, print R2.


# THE CLEAN PATH
# Split first, compute the correlations on training only, select the five
# from that, train, print R2.
