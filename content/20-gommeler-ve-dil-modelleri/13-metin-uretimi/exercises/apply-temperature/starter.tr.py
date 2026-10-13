def apply_temperature(probs, t):
    return {}

probs = {"order": 0.6, "parcel": 0.3, "box": 0.1}
for t in [0.5, 1.0, 2.0]:
    result = apply_temperature(probs, t)
    print(t, " ".join(f"{w}={x}" for w, x in result.items()))
