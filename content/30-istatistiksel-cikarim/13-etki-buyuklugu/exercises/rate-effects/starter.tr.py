def rate_effects(p_a, p_b):
    diff = round(p_b - p_a, 4)
    return [diff, diff, diff]


print(rate_effects(0.10, 0.12))
print(rate_effects(0.40, 0.48))
