from scipy import stats
from ab_data import make_population

users = make_population()
visits = users["visits"]
share = visits.value_counts(normalize=True).sort_index()
model = stats.poisson(mu=visits.mean())
for k in range(6):
    print(k, round(share[k], 3), round(float(model.pmf(k)), 3))
print(round(visits.mean(), 2), round(visits.var(), 2))
