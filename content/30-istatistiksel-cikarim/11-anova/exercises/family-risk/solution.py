def family_risk(k, alpha):
    pairs = k * (k - 1) // 2
    return [pairs, round(1 - (1 - alpha) ** pairs, 3)]


print(family_risk(4, 0.05))
print(family_risk(10, 0.05))
