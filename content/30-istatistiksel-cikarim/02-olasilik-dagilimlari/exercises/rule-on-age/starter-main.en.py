from scipy import stats
from ab_data import make_population

users = make_population()
x = users["age"]
# For k = 1, 2, 3 on one line: k, the normal distribution's share within
# k deviations of the mean and the real share of ages in that range
# (4 places).
