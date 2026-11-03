from statsmodels.stats.proportion import proportions_ztest
from ab_data import make_ramp_test

ramp = make_ramp_test(seed=11)
# 1) Print the total buying rates (A first, then B; 4 places).
# 2) Print the rates of the second week only (week == 2) the same way.
# 3) Print the two-proportion z-test p for the second week, 3 places
#    (proportions_ztest, B first then A).
