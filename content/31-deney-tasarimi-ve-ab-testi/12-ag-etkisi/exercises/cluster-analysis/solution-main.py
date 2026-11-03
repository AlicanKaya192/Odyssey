from scipy import stats
from ab_data import make_market

cities = make_market(seed=22, design="city")
per_city = cities.groupby(["city", "group"])["completed"].mean().reset_index()
b = per_city.loc[per_city["group"] == "B", "completed"]
a = per_city.loc[per_city["group"] == "A", "completed"]
print(round(float(stats.ttest_ind(b, a, equal_var=False).pvalue), 3))
ub = cities.loc[cities["group"] == "B", "completed"]
ua = cities.loc[cities["group"] == "A", "completed"]
print(round(float(stats.ttest_ind(ub, ua, equal_var=False).pvalue), 3))
