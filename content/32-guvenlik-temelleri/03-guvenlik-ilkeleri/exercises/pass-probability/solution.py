def pass_probability(layers):
    chance = 1.0
    for p in layers:
        chance *= p
    return round(chance, 4)

print(pass_probability([0.3, 0.2, 0.1]))
print(pass_probability([0.5]))
print(pass_probability([]))
