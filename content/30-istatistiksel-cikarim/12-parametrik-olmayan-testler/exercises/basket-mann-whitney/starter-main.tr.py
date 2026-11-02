import numpy as np
from scipy import stats
from ab_data import make_basket_test

test = make_basket_test(n=150, seed=211)
a = test.loc[test["group"] == "A", "basket"].to_numpy()
b = test.loc[test["group"] == "B", "basket"].to_numpy()
print(round(np.median(a), 1), round(np.median(b), 1))
# 1) stats.mannwhitneyu(b, a) ile p'yi 4 basamakla yazdır.
# 2) Ortak dil etki büyüklüğünü U / (n_A * n_B) 3 basamakla yazdır.
