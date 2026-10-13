def top_p_filter(probs, p):
    return {}

probs = {"order": 0.5, "parcel": 0.3, "box": 0.15, "app": 0.05}
for p in [0.75, 0.4, 1.0]:
    result = top_p_filter(probs, p)
    print(p, " ".join(f"{w}={x}" for w, x in result.items()))
