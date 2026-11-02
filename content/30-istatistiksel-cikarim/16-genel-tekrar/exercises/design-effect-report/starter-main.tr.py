import numpy as np
from scipy import stats
from ab_data import make_design_test

test = make_design_test(n=200, seed=612)
a = test.loc[test["group"] == "A", "minutes"].to_numpy()
b = test.loc[test["group"] == "B", "minutes"].to_numpy()
# Alt alta yaz:
# 1) iki medyan (2 basamak)
# 2) Welch t-testinin p'si, 3) Mann-Whitney'in p'si (4 basamak)
# 4) Cohen's d (3 basamak); gruplar eşit büyüklükte, birleşik sapma
#    np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
