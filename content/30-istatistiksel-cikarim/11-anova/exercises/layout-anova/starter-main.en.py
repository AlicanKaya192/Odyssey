from scipy import stats
from ab_data import make_layout_test

test = make_layout_test(n=80, seed=181)
means = test.groupby("layout")["minutes"].mean().round(2)
print(means.to_dict())
# Make each layout's times a separate array:
# groups = [g["minutes"] for _, g in test.groupby("layout")]
# Print F (3 places) and p (4 places) from stats.f_oneway(*groups).
