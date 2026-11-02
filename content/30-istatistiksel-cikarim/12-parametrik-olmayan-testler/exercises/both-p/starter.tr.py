from scipy import stats


def both_p(a, b):
    p_t = stats.ttest_ind(b, a, equal_var=False).pvalue
    return [round(float(p_t), 4), round(float(p_t), 4)]


a = [42, 55, 61, 48, 70, 52, 66, 58]
b = [68, 75, 81, 72, 90, 77, 85, 79, 900]
print(both_p(a, b))
