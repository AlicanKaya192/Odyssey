from scipy import stats
from ab_data import make_assignment_log

log = make_assignment_log(n=50000, seed=744, lost_b=0.1)
counts = log["group"].value_counts().sort_index()
# 1) Print the SRM test's p formatted as f"{p:.1e}".
# 2) Print the difference of buying rates (B - A) with 4 places.
