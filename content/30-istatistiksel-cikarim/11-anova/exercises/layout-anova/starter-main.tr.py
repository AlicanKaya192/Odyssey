from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=80, seed=181)
means = test.groupby("layout")["minutes"].mean().round(2)
print(means.to_dict())
# Her düzenin süreleri ayrı bir dizi olsun:
# groups = [g["minutes"] for _, g in test.groupby("layout")]
# stats.f_oneway(*groups) ile F (3 basamak) ve p'yi (4 basamak) yazdır.
