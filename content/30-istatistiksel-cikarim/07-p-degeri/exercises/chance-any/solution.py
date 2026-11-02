def chance_any(k, alpha):
    return round(1 - (1 - alpha) ** k, 3)


print(chance_any(1, 0.05))
print(chance_any(20, 0.05))
