from scipy import stats
from ab_data import make_population

users = make_population()
visits = users["visits"]
# 1) For each k = 0..5: k, the real share and the Poisson model's pmf
#    (both with 3 places).
# 2) On the last line, the mean and the variance (2 places).
