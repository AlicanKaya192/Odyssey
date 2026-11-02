def rate_effects(p_a, p_b):
    odds_a = p_a / (1 - p_a)
    odds_b = p_b / (1 - p_b)
    return [round(p_b - p_a, 4), round(p_b / p_a, 3),
            round(odds_b / odds_a, 3)]


print(rate_effects(0.10, 0.12))
print(rate_effects(0.40, 0.48))
