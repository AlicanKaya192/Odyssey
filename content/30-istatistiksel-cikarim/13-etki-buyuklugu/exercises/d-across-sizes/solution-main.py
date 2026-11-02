import numpy as np
from scipy import stats
from ab_data import make_design_test


def cohens_d(a, b):
    na, nb = len(a), len(b)
    pooled_var = ((na - 1) * a.var(ddof=1)
                  + (nb - 1) * b.var(ddof=1)) / (na + nb - 2)
    return (b.mean() - a.mean()) / np.sqrt(pooled_var)


for n in [50, 500, 5000]:
    test = make_design_test(n=n, seed=311)
    a = test.loc[test["group"] == "A", "minutes"].to_numpy()
    b = test.loc[test["group"] == "B", "minutes"].to_numpy()
    p = stats.ttest_ind(b, a, equal_var=False).pvalue
    print(n, round(cohens_d(a, b), 3), f"{p:.1e}")
