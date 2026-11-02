from scipy import stats


def t_multiplier(level, n):
    return round(float(stats.norm.ppf((1 + level) / 2)), 3)


print(t_multiplier(0.95, 5))
print(t_multiplier(0.95, 100))
print(t_multiplier(0.99, 20))
