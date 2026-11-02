from scipy import stats
from ab_data import make_paired_speed

pages = make_paired_speed(n=20, seed=212)
print(round(stats.ttest_rel(pages["before"], pages["after"]).pvalue, 4))
print(round(stats.wilcoxon(pages["before"], pages["after"]).pvalue, 4))
