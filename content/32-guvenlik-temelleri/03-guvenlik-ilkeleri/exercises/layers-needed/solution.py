def layers_needed(pass_prob, target):
    if pass_prob >= 1:
        return None
    count = 1
    chance = pass_prob
    while chance > target:
        count += 1
        chance *= pass_prob
    return count

print(layers_needed(0.3, 0.01))
print(layers_needed(0.5, 0.001))
print(layers_needed(1.0, 0.1))
