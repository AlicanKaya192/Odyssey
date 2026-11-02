from scipy import stats
from ab_data import make_population

users = make_population()
x = users["age"]
for k in [1, 2, 3]:
    model = float(stats.norm.cdf(k) - stats.norm.cdf(-k))
    real = float(((x - x.mean()).abs() <= k * x.std()).mean())
    print(k, round(model, 4), round(real, 4))
