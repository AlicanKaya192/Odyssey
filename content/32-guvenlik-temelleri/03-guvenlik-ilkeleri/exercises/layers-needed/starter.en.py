def layers_needed(pass_prob, target):
    # start with one layer, add more until the chance reaches the target
    return 0

print(layers_needed(0.3, 0.01))
print(layers_needed(0.5, 0.001))
print(layers_needed(1.0, 0.1))
