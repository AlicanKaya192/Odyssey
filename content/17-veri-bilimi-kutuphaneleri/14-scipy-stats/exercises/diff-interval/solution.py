from scipy import stats


def diff_interval(a, b):
    res = stats.ttest_ind(b, a, equal_var=False)
    low, high = res.confidence_interval(confidence_level=0.95)
    return [round(float(low), 2), round(float(high), 2), bool(low <= 0 <= high)]

A = [52.1, 48.3, 55.0, 61.2, 47.5, 50.8, 58.9, 44.2, 53.7, 49.9]
B = [60.4, 71.8, 45.2, 80.1, 66.3, 52.7, 77.9, 58.0]
print(diff_interval(A, B))
