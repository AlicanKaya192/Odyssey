def should_promote(candidate, current, min_gain):
    # Is there a measurement, is there a version in production, is the gain enough?
    pass


print(should_promote({"accuracy": 0.82}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.812}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.79}, None, 0.003))
print(should_promote({"loss": 0.4}, {"accuracy": 0.81}, 0.003))
