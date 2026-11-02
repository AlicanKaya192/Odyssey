from scipy import stats
from ab_data import make_assignment_log

log = make_assignment_log(n=40000, seed=743, lost_b=0.08)
c = log["group"].value_counts().sort_index()
print(c.to_dict(), f"{stats.chisquare(c).pvalue:.1e}")
