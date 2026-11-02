from scipy import stats


def paired_p(before, after):
    diffs = [b - a for b, a in zip(before, after)]
    return round(float(stats.ttest_1samp(diffs, 0).pvalue), 4)


print(paired_p([910, 860, 845, 930, 880], [890, 851, 820, 915, 866]))
