def should_promote(candidate, current, min_gain):
    # Olcum var mi, canlida surum var mi, kazanc yeterli mi?
    pass


print(should_promote({"accuracy": 0.82}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.812}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.79}, None, 0.003))
print(should_promote({"loss": 0.4}, {"accuracy": 0.81}, 0.003))
