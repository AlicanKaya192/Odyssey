from scipy import stats


def paired_p(before, after):
    mean_after = sum(after) / len(after)
    return round(float(stats.ttest_1samp(before, mean_after).pvalue), 4)


print(paired_p([910, 860, 845, 930, 880], [890, 851, 820, 915, 866]))
