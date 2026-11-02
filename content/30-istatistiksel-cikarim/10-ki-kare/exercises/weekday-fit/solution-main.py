from scipy import stats
from ab_data import make_weekday_orders

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
observed = make_weekday_orders(n=700, seed=161).value_counts().reindex(days)
result = stats.chisquare(observed)
print(observed.tolist())
print(round(result.statistic, 2), round(result.pvalue, 4))
