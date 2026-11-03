from scipy import stats
from ab_data import make_market

cities = make_market(seed=22, design="city")
# 1) Print the Welch p with city means (each city one observation), with 3
#    places.
# 2) Print the Welch p that treats the users of the same data as independent.
