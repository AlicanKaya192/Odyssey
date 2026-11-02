from scipy import stats
from ab_data import make_assignment_log

log = make_assignment_log(n=50000, seed=744, lost_b=0.1)
counts = log["group"].value_counts().sort_index()
# 1) SRM testinin p'sini f"{p:.1e}" biçiminde yazdır.
# 2) Satın alma oranlarının farkını (B - A) 4 basamakla yazdır.
