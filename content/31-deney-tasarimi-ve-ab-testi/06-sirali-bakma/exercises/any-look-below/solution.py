def any_below(p_values, threshold=0.05):
    return any(p < threshold for p in p_values)


print(any_below([0.3, 0.04, 0.2, 0.08]))
print(any_below([0.3, 0.04, 0.2, 0.08], 0.01))
