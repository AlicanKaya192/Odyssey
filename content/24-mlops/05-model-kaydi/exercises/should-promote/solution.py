def should_promote(candidate, current, min_gain):
    if "accuracy" not in candidate:
        return "keep"
    if current is None:
        return "promote"
    if candidate["accuracy"] - current["accuracy"] >= min_gain:
        return "promote"
    return "keep"


print(should_promote({"accuracy": 0.82}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.812}, {"accuracy": 0.81}, 0.003))
print(should_promote({"accuracy": 0.79}, None, 0.003))
print(should_promote({"loss": 0.4}, {"accuracy": 0.81}, 0.003))
