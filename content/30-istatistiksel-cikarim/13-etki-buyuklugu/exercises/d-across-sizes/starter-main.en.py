import numpy as np
from scipy import stats
from ab_data import make_design_test


def cohens_d(a, b):
    na, nb = len(a), len(b)
    pooled_var = ((na - 1) * a.var(ddof=1)
                  + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    return (b.mean() - a.mean()) / np.sqrt(pooled_var)


# For n = 50, 500, 5000 build make_design_test(n=n, seed=311) and print on
# each line n, d (3 places) and Welch's p formatted as f"{p:.1e}".
