from scipy import stats
from ab_data import make_paired_speed

pages = make_paired_speed(n=15, seed=122)
diff = pages["before"] - pages["after"]
print(round(diff.mean(), 1))
print(round(stats.ttest_ind(pages["before"], pages["after"]).pvalue, 4))
