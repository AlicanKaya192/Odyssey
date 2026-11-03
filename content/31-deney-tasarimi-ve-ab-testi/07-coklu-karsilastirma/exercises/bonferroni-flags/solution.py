def bonferroni_flags(p_values, alpha=0.05):
    m = len(p_values)
    return [p < alpha / m for p in p_values]


print(bonferroni_flags([0.001, 0.02, 0.04, 0.3]))
