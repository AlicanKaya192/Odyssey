from scipy import stats
from ab_data import make_assignment_log

log = make_assignment_log(n=50000, seed=744, lost_b=0.1)
counts = log["group"].value_counts().sort_index()
print(f"{stats.chisquare(counts).pvalue:.1e}")
rates = log.groupby("group")["bought"].mean()
print(round(rates["B"] - rates["A"], 4))
