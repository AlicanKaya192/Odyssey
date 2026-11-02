from scipy import stats
from ab_data import make_assignment_log

log = make_assignment_log(n=40000, seed=743, lost_b=0.08)
for platform, part in log.groupby("platform"):
    c = part["group"].value_counts().sort_index()
    print(platform, f"{stats.chisquare(c).pvalue:.1e}")
