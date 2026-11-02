from scipy import stats


def decide(values, mu0, alpha):
    p = float(stats.ttest_1samp(values, mu0).pvalue)
    if p < alpha:
        return ["reject", round(p, 4)]
    return ["keep", round(p, 4)]


print(decide([910, 860, 845, 930, 880, 905, 870, 925], 850, 0.05))
print(decide([852, 848, 851, 849, 853, 847], 850, 0.05))
