def top_k_filter(probs, k):
    return {}

probs = {"order": 0.5, "parcel": 0.3, "box": 0.15, "app": 0.05}
for k in [2, 1]:
    result = top_k_filter(probs, k)
    print(k, " ".join(f"{w}={x}" for w, x in result.items()))
